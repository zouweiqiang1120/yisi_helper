package com.example.yisi_helper

import android.app.Service
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.util.Log
import android.view.Gravity
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.SeekBar
import android.widget.TextView

/**
 * 增强版悬浮窗服务
 * 支持透明度调节和缩放控制
 */
class FloatingWindowService : Service() {
    companion object {
        const val TAG = "FloatingWindow"
        private var windowManager: WindowManager? = null
        private var floatingView: View? = null
        private var layoutParams: WindowManager.LayoutParams? = null
        
        // 当前状态
        private var currentAlpha = 0.9f  // 默认透明度
        private var currentScale = 1.0f  // 默认缩放
        private var isMinimized = false
        
        fun updateQuestionData(context: Context, data: QuestionData) {
            val intent = Intent("com.example.yisi_helper.UPDATE_DATA")
            intent.putExtra("question", data.question)
            intent.putExtra("options", data.options.map { "${it.label}:${it.content}" }.toTypedArray())
            context.sendBroadcast(intent)
        }

        fun updateAnswer(context: Context, answerText: String, answerLabel: String) {
            val intent = Intent("com.example.yisi_helper.UPDATE_ANSWER")
            intent.putExtra("answerText", answerText)
            intent.putExtra("answerLabel", answerLabel)
            context.sendBroadcast(intent)
        }
    }

    private val broadcastReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            when (intent?.action) {
                "com.example.yisi_helper.UPDATE_DATA" -> {
                    val question = intent.getStringExtra("question") ?: return
                    val optionsArray = intent.getStringArrayExtra("options") ?: return
                    val options = optionsArray.map {
                        val parts = it.split(":", limit = 2)
                        OptionData(parts[0], parts.getOrElse(1) { "" })
                    }
                    updateQuestionDisplay(question, options)
                }
                "com.example.yisi_helper.UPDATE_ANSWER" -> {
                    val answerText = intent.getStringExtra("answerText") ?: return
                    val answerLabel = intent.getStringExtra("answerLabel") ?: return
                    updateAnswerDisplay(answerText, answerLabel)
                }
            }
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        
        val filter = IntentFilter().apply {
            addAction("com.example.yisi_helper.UPDATE_DATA")
            addAction("com.example.yisi_helper.UPDATE_ANSWER")
        }
        registerReceiver(broadcastReceiver, filter)
        
        Log.d(TAG, "悬浮窗服务创建")
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (floatingView == null) {
            createFloatingWindow()
        }
        return START_STICKY
    }

    private fun createFloatingWindow() {
        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        
        val inflater = LayoutInflater.from(this)
        floatingView = inflater.inflate(R.layout.floating_window_enhanced, null)
        
        layoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            } else {
                WindowManager.LayoutParams.TYPE_PHONE
            },
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 50
            y = 100
        }
        
        setupControls()
        setupDrag()
        
        windowManager?.addView(floatingView, layoutParams)
        Log.d(TAG, "悬浮窗已创建")
    }

    private fun setupControls() {
        // 关闭按钮
        floatingView?.findViewById<ImageButton>(R.id.btn_close)?.setOnClickListener {
            stopSelf()
        }
        
        // 最小化/展开按钮
        floatingView?.findViewById<ImageButton>(R.id.btn_toggle)?.setOnClickListener {
            toggleMinimize()
        }
        
        // 透明度调节
        floatingView?.findViewById<SeekBar>(R.id.seekbar_alpha)?.apply {
            progress = (currentAlpha * 100).toInt()
            setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
                override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                    currentAlpha = progress / 100f
                    updateAlpha()
                }
                override fun onStartTrackingTouch(seekBar: SeekBar?) {}
                override fun onStopTrackingTouch(seekBar: SeekBar?) {}
            })
        }
        
        // 缩放调节
        floatingView?.findViewById<SeekBar>(R.id.seekbar_scale)?.apply {
            progress = ((currentScale - 0.5f) * 100).toInt()
            setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
                override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                    currentScale = 0.5f + (progress / 100f)
                    updateScale()
                }
                override fun onStartTrackingTouch(seekBar: SeekBar?) {}
                override fun onStopTrackingTouch(seekBar: SeekBar?) {}
            })
        }
    }

    private fun setupDrag() {
        val dragHandle = floatingView?.findViewById<View>(R.id.drag_handle)
        
        dragHandle?.setOnTouchListener(object : View.OnTouchListener {
            private var initialX = 0
            private var initialY = 0
            private var touchX = 0f
            private var touchY = 0f

            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = layoutParams?.x ?: 0
                        initialY = layoutParams?.y ?: 0
                        touchX = event.rawX
                        touchY = event.rawY
                        return true
                    }
                    MotionEvent.ACTION_MOVE -> {
                        val dx = event.rawX - touchX
                        val dy = event.rawY - touchY
                        layoutParams?.x = initialX + dx.toInt()
                        layoutParams?.y = initialY + dy.toInt()
                        windowManager?.updateViewLayout(floatingView, layoutParams)
                        return true
                    }
                }
                return false
            }
        })
    }

    private fun toggleMinimize() {
        isMinimized = !isMinimized
        
        val contentLayout = floatingView?.findViewById<LinearLayout>(R.id.layout_content)
        val toggleBtn = floatingView?.findViewById<ImageButton>(R.id.btn_toggle)
        
        if (isMinimized) {
            contentLayout?.visibility = View.GONE
            toggleBtn?.setImageResource(android.R.drawable.arrow_up_float)
        } else {
            contentLayout?.visibility = View.VISIBLE
            toggleBtn?.setImageResource(android.R.drawable.arrow_down_float)
        }
    }

    private fun updateAlpha() {
        floatingView?.alpha = currentAlpha
    }

    private fun updateScale() {
        floatingView?.scaleX = currentScale
        floatingView?.scaleY = currentScale
    }

    private fun updateQuestionDisplay(question: String, options: List<OptionData>) {
        val questionText = floatingView?.findViewById<TextView>(R.id.tv_question)
        val optionsText = floatingView?.findViewById<TextView>(R.id.tv_options)
        
        questionText?.text = question.take(50) + if (question.length > 50) "..." else ""
        
        // 显示选项内容
        val optionsStr = options.joinToString("\n") { "${it.label}. ${it.content}" }
        optionsText?.text = optionsStr
    }

    private fun updateAnswerDisplay(answerText: String, answerLabel: String) {
        val answerTextView = floatingView?.findViewById<TextView>(R.id.tv_answer)
        val answerDetailView = floatingView?.findViewById<TextView>(R.id.tv_answer_detail)
        
        // 显示选项标签
        answerTextView?.text = "答案: $answerLabel"
        
        // 显示选项内容
        answerDetailView?.text = answerText
        answerDetailView?.visibility = View.VISIBLE
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(broadcastReceiver)
        floatingView?.let {
            windowManager?.removeView(it)
        }
        floatingView = null
        Log.d(TAG, "悬浮窗服务销毁")
    }
}
