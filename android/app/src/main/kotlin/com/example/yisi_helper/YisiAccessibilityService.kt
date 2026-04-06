package com.example.yisi_helper

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.AccessibilityServiceInfo
import android.content.Intent
import android.os.Build
import android.util.Log
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledExecutorService
import java.util.concurrent.TimeUnit
import java.util.concurrent.ConcurrentHashMap

/**
 * 极速版无障碍服务
 * 优化：快速响应 + 准确匹配
 */
class YisiAccessibilityService : AccessibilityService() {
    companion object {
        const val TAG = "YisiAccessibility"
        const val CHANNEL = "com.example.yisi_helper/accessibility"
        var instance: YisiAccessibilityService? = null
        
        // 极速响应配置
        const val FAST_RESPONSE_DELAY = 100L  // 100ms极速响应
        const val DEBOUNCE_DELAY = 300L       // 300ms防抖
        
        // 缓存配置
        const val CACHE_SIZE = 50             // 缓存最近50道题
    }

    private var lastTextHash: Int = 0
    private var lastProcessTime: Long = 0
    private val executor: ScheduledExecutorService = Executors.newSingleThreadScheduledExecutor()
    private var pendingTask: java.util.concurrent.ScheduledFuture<*>? = null
    
    // 题目缓存（加速重复题目）
    private val questionCache = ConcurrentHashMap<Int, QuestionData>()
    private var cacheHits = 0
    private var cacheMisses = 0

    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
        
        val info = AccessibilityServiceInfo().apply {
            // 监听更多事件类型，确保快速捕获
            eventTypes = 
                AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED or
                AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED or
                AccessibilityEvent.TYPE_VIEW_FOCUSED or
                AccessibilityEvent.TYPE_VIEW_CLICKED or
                AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED or
                AccessibilityEvent.TYPE_VIEW_SCROLLED
            
            feedbackType = AccessibilityServiceInfo.FEEDBACK_GENERIC
            
            // 优化标志
            flags = 
                AccessibilityServiceInfo.FLAG_REPORT_VIEW_IDS or
                AccessibilityServiceInfo.FLAG_RETRIEVE_INTERACTIVE_WINDOWS or
                AccessibilityServiceInfo.FLAG_INCLUDE_NOT_IMPORTANT_VIEWS
            
            // 目标APP包名
            packageNames = arrayOf(
                "com.eastsim.nettrmp.v35",
                "com.eastsim.nettrmp.android"
            )
            
            // 极短的通知超时，快速响应
            notificationTimeout = 50L
        }
        serviceInfo = info
        
        Log.d(TAG, "极速版无障碍服务已启动")
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        event ?: return
        
        // 快速过滤：只处理特定事件
        when (event.eventType) {
            AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED,
            AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED,
            AccessibilityEvent.TYPE_VIEW_FOCUSED -> {
                processEventFast(event)
            }
        }
    }

    private fun processEventFast(event: AccessibilityEvent) {
        // 取消之前的任务
        pendingTask?.cancel(false)
        
        // 立即执行（极速模式）
        pendingTask = executor.schedule({
            extractAndMatch(event)
        }, FAST_RESPONSE_DELAY, TimeUnit.MILLISECONDS)
    }

    private fun extractAndMatch(event: AccessibilityEvent) {
        try {
            val rootNode = rootInActiveWindow ?: return
            
            // 快速包名检查
            val packageName = event.packageName?.toString()
            if (packageName == null || !packageName.contains("eastsim")) {
                rootNode.recycle()
                return
            }
            
            // 极速提取题目数据
            val screenData = extractQuestionDataFast(rootNode)
            rootNode.recycle()
            
            if (screenData.question.isEmpty()) return
            
            // 计算内容哈希
            val contentHash = calculateHash(screenData)
            
            // 检查是否重复
            if (contentHash == lastTextHash) return
            lastTextHash = contentHash
            
            // 检查缓存
            val cachedResult = questionCache[contentHash]
            if (cachedResult != null) {
                cacheHits++
                Log.d(TAG, "缓存命中! 直接返回答案")
                sendDataToFlutter(cachedResult, true)
                return
            }
            
            cacheMisses++
            
            // 发送到Flutter进行匹配
            Log.d(TAG, "新题目，发送到匹配引擎: ${screenData.question.take(30)}...")
            sendDataToFlutter(screenData, false)
            
            // 添加到缓存
            if (questionCache.size >= CACHE_SIZE) {
                questionCache.clear() // 简单清空，可优化为LRU
            }
            questionCache[contentHash] = screenData
            
        } catch (e: Exception) {
            Log.e(TAG, "处理出错: ${e.message}")
        }
    }

    /**
     * 极速提取题目数据
     */
    private fun extractQuestionDataFast(node: AccessibilityNodeInfo): QuestionData {
        val questionBuilder = StringBuilder()
        val options = mutableListOf<OptionData>()
        
        // 使用栈而非递归，提高速度
        val stack = ArrayDeque<AccessibilityNodeInfo>()
        stack.add(node)
        
        while (stack.isNotEmpty()) {
            val current = stack.removeLast()
            
            // 提取文本
            current.text?.let { text ->
                val str = text.toString().trim()
                if (str.isNotEmpty()) {
                    processTextFast(str, questionBuilder, options)
                }
            }
            
            // 添加子节点到栈
            for (i in current.childCount - 1 downTo 0) {
                current.getChild(i)?.let { child ->
                    stack.add(child)
                }
            }
            
            // 回收节点（非根节点）
            if (current != node) {
                current.recycle()
            }
        }
        
        return QuestionData(
            question = questionBuilder.toString().trim(),
            options = options
        )
    }

    /**
     * 快速处理文本
     */
    private fun processTextFast(
        text: String,
        questionBuilder: StringBuilder,
        options: MutableList<OptionData>
    ) {
        // 快速检测选项 (A. 或 A、 开头)
        if (text.length >= 2 && text[0] in 'A'..'D') {
            val separator = text[1]
            if (separator == '.' || separator == '．' || separator == '、' || separator == ' ') {
                val content = text.substring(2).trim()
                if (content.isNotEmpty()) {
                    options.add(OptionData(text[0].toString(), content))
                    return
                }
            }
        }
        
        // 检测题目（包含括号或问号）
        if (text.contains("（）") || text.contains("()") || 
            text.contains("？") || text.contains("?")) {
            questionBuilder.append(text).append(" ")
        }
    }

    /**
     * 计算内容哈希（快速版）
     */
    private fun calculateHash(data: QuestionData): Int {
        var hash = data.question.hashCode()
        for (opt in data.options) {
            hash = hash * 31 + opt.content.hashCode()
        }
        return hash
    }

    /**
     * 发送数据到Flutter
     */
    private fun sendDataToFlutter(data: QuestionData, fromCache: Boolean) {
        val intent = Intent("com.example.yisi_helper.SCREEN_DATA")
        intent.putExtra("question", data.question)
        intent.putExtra("options", data.options.map { "${it.label}:${it.content}" }.toTypedArray())
        intent.putExtra("fromCache", fromCache)
        intent.putExtra("timestamp", System.currentTimeMillis())
        
        sendBroadcast(intent)
        
        // 更新悬浮窗
        FloatingWindowService.updateQuestionData(this, data)
    }

    override fun onInterrupt() {
        Log.d(TAG, "服务中断")
        pendingTask?.cancel(false)
    }

    override fun onDestroy() {
        super.onDestroy()
        executor.shutdown()
        pendingTask?.cancel(false)
        questionCache.clear()
        Log.d(TAG, "服务销毁，缓存命中率: ${if(cacheHits+cacheMisses>0) cacheHits*100/(cacheHits+cacheMisses) else 0}%")
    }

    /**
     * 获取缓存统计
     */
    fun getCacheStats(): Pair<Int, Int> = Pair(cacheHits, cacheMisses)
}

/**
 * 题目数据
 */
data class QuestionData(
    val question: String,
    val options: List<OptionData>
)

/**
 * 选项数据
 */
data class OptionData(
    val label: String,
    val content: String
)
