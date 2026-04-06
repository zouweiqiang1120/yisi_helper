// 完整的LLDPE装置操作工考试题库
// 本文件包含从提供的文本中提取的所有题目
// 由于题目数量较多，这里采用分段存储方式

// 第一部分：装置概况与工艺流程
const List<Map<String, dynamic>> questionsPart1 = [
  {"content": "LLDPE装置常见的产能规模表述单位是（）。", "options": ["万吨/年", "立方米/小时", "吨/小时", "千克/分钟"], "answer": "A", "type": "single"},
  {"content": "LLDPE装置中负责将粉料加工成颗粒产品的单元是（）。", "options": ["造粒单元", "聚合单元", "精制单元", "储存单元"], "answer": "A", "type": "single"},
  {"content": "某LLDPE装置进料量为180m³/h，负荷率为90%，其设计进料量为（）m³/h。", "options": ["162", "200", "198", "220"], "answer": "B", "type": "single"},
  {"content": "LLDPE装置通常由哪些主要单元组成（）。", "options": ["精制单元", "聚合单元", "造粒单元", "辅助公用工程单元"], "answer": "A;B;C;D", "type": "multiple"},
  {"content": "装置转产前确认产能规模相关的条件包括（）。", "options": ["反应所需原料充足且质量稳定", "造粒工段做好转产准备", "后工序及相关单位得到通知", "设备负荷能力满足转产要求"], "answer": "A;B;C;D", "type": "multiple"},
  {"content": "LLDPE装置的产能规模仅由反应器的大小决定。", "options": ["对", "错", "", ""], "answer": "B", "type": "judge"},
  {"content": "45万吨/年LLDPE装置是指该装置每年能生产45万吨线性低密度聚乙烯产品。", "options": ["对", "错", "", ""], "answer": "A", "type": "judge"},
  {"content": "装置转产前无需确认后工序的产能匹配情况。", "options": ["对", "错", "", ""], "answer": "B", "type": "judge"},
];

// 第二部分：原料与催化剂
const List<Map<String, dynamic>> questionsPart2 = [
  {"content": "异戊烷在LLDPE装置中的主要作用是作为（）。", "options": ["诱导冷凝剂", "反应组分", "溶剂", "无任何作用"], "answer": "A", "type": "single"},
  {"content": "丁烯精制后，要求水含量小于（）PPm。", "options": ["1", "0.1", "10", "5"], "answer": "B", "type": "single"},
  {"content": "乙烯干燥器预负荷时，床层温度不能超过（）℃。", "options": ["110", "100", "90", "120"], "answer": "B", "type": "single"},
  {"content": "己烯脱气塔正常操作压力是（）MPa。", "options": ["0.48", "0.58", "0.175", "0.20"], "answer": "C", "type": "single"},
  {"content": "LLDPE装置原料精制系统主要包括的原料精制过程有（）。", "options": ["乙烯精制", "丁烯-1/己烯-1精制", "氮气精制", "异戊烷精制"], "answer": "A;B;C;D", "type": "multiple"},
  {"content": "UNIPOL聚乙烯工艺中原料相关的安全性优势包括（）。", "options": ["原料相对无毒", "无需反应溶剂", "减少可燃液体处理危险", "操作条件适中"], "answer": "A;B;C;D", "type": "multiple"},
  {"content": "原料精制系统的目的是脱除原料中的各类杂质，以满足聚合反应的原料质量要求。", "options": ["对", "错", "", ""], "answer": "A", "type": "judge"},
  {"content": "UNIPOL聚乙烯工艺用单一反应器可在生产能力不变时生产不同密度的聚乙烯产品。", "options": ["对", "错", "", ""], "answer": "A", "type": "judge"},
  {"content": "丁烯进干燥器前要求达到30℃。", "options": ["对", "错", "", ""], "answer": "A", "type": "judge"},
  {"content": "乙烯干燥器预负荷时，床层温度不能超过100℃。", "options": ["对", "错", "", ""], "answer": "A", "type": "judge"},
];

// 第三部分：反应系统
const List<Map<String, dynamic>> questionsPart3 = [
  {"content": "LLDPE装置的核心产品是（）。", "options": ["线性低密度聚乙烯树脂", "高密度聚乙烯树脂", "聚丙烯树脂", "聚氯乙烯树脂"], "answer": "A", "type": "single"},
  {"content": "LLDPE装置中，共聚单体丁烯-1进入反应器常见来源是（）。", "options": ["装置内共聚单体精制单元", "乙烯裂解装置副产", "外购液态丁烯-1", "催化剂分解产物"], "answer": "A", "type": "single"},
  {"content": "LLDPE装置中，乙烯原料的主要来源通常是（）。", "options": ["共聚单体干燥系统", "装置内脱气塔产出", "催化剂配制单元", "界区外乙烯裂解装置"], "answer": "D", "type": "single"},
  {"content": "循环气压缩机是一台单级、恒速的（）式压缩机。", "options": ["往复", "离心", "轴流", "螺杆"], "answer": "B", "type": "single"},
  {"content": "CO作为LLDPE装置催化剂的毒物类型是（）。", "options": ["不可逆", "可逆", "永久性", "腐蚀性"], "answer": "B", "type": "single"},
  {"content": "使用UCAT-J作为主催化剂时，必须使用的助催化剂消杂的是（）。", "options": ["T1", "T2", "T3", "T4"], "answer": "B", "type": "single"},
  {"content": "影响聚合反应速率的主要因素包括（）。", "options": ["催化剂活性", "反应温度", "乙烯进料浓度", "共聚单体比例"], "answer": "A;B;C;D", "type": "multiple"},
  {"content": "乙烯精制过程中需要脱除的杂质有（）。", "options": ["水分", "氧气", "一氧化碳", "甲醇"], "answer": "A;B;C;D", "type": "multiple"},
  {"content": "低密度聚乙烯与高密度聚乙烯的物理化学特性完全相同。", "options": ["对", "错", "", ""], "answer": "B", "type": "judge"},
  {"content": "生产正常时无需定时对聚合单元的工艺参数及设备运行状态进行巡检。", "options": ["对", "错", "", ""], "answer": "B", "type": "judge"},
  {"content": "长期吸入高浓度的己烷蒸汽，会引起神经麻痹和神经衰弱等健康问题。", "options": ["对", "错", "", ""], "answer": "A", "type": "judge"},
];

// 第四部分：PID图与仪表
const List<Map<String, dynamic>> questionsPart4 = [
  {"content": "炼油化工PID图中，标注"PCV-101"的仪表表示（）。", "options": ["101号温度变送器", "101号压力控制阀", "101号流量开关", "101号切断阀"], "answer": "B", "type": "single"},
  {"content": "LLDPE装置PID图中，控制循环气流量的调节阀通常标注的符号是（）。", "options": ["带'PV'标识的阀门", "带'TV'标识的阀门", "带'FV'标识的阀门", "带'LV'标识的阀门"], "answer": "C", "type": "single"},
  {"content": "LLDPE装置PID图中，符号'FIC-301'表示的仪表功能是（）。", "options": ["流量指示报警", "流量指示控制", "温度指示控制", "压力指示调节"], "answer": "B", "type": "single"},
  {"content": "LLDPE装置PID图中，下列仪表符号的功能描述正确的有（）。", "options": ["FT代表流量变送器", "TT代表温度变送器", "PT代表压力调节阀", "FIC代表流量指示控制器"], "answer": "A;B;D", "type": "multiple"},
  {"content": "LLDPE装置PID图中会标注主要设备的位号及名称，如反应器C-4001、循环气压缩机K-4003。", "options": ["对", "错", "", ""], "answer": "A", "type": "judge"},
  {"content": "LLDPE装置PID图中，管线箭头方向通常表示介质的正常流动方向。", "options": ["对", "错", "", ""], "answer": "A", "type": "judge"},
];

// 第五部分：精制单元
const List<Map<String, dynamic>> questionsPart5 = [
  {"content": "共聚单体干燥床出口的在线分析仪测得水含量需小于（）时，系统具备向聚合单元送料的条件。", "options": ["0.5μg/g", "0.1μg/g", "1.0μg/g", "2.0μg/g"], "answer": "B", "type": "single"},
  {"content": "丁烯进料泵打小循环时，物流的走向是泵出口→（）→C-1008。", "options": ["火炬排放管线", "干燥床C-1004", "FICA-1002-1旁路管线", "原料油储罐V-1008"], "answer": "C", "type": "single"},
  {"content": "异戊烷精制系统启动泵打循环时，泵出口物料经FV-1412-1旁路返回的设备是（）。", "options": ["1213-C-1419", "1213-C-1406", "1213-E-1011", "1213-G-1412"], "answer": "B", "type": "single"},
  {"content": "丁烯脱气塔正常操作压力是（）MPa。", "options": ["0.58", "0.381", "0.17", "0.20"], "answer": "B", "type": "single"},
];

// 第六部分：反应系统操作
const List<Map<String, dynamic>> questionsPart6 = [
  {"content": "调温水系统实现循环的动力设备是（）。", "options": ["1213-K-4003", "1213-G-4004和1213-G-4005", "1213-G-5001", "1213-P-4001"], "answer": "B", "type": "single"},
  {"content": "启动循环气压缩机后，体现控制循环气表观气速的设备是（）。", "options": ["FV-4001-1", "1213-HIC-4003-3", "HV-4001-58", "HV-4001-95"], "answer": "B", "type": "single"},
  {"content": "氢气引入系统中，进反应器前向火炬排放的位置位于（）之后。", "options": ["FV-4001-3", "HV-4001-6", "HV-4001-58", "FV-4001-1"], "answer": "B", "type": "single"},
  {"content": "循环气压缩机出现电力故障时会触发的终止类型是（）。", "options": ["Ⅰ型终止", "Ⅱ型终止", "小型终止", "Ⅲ型终止"], "answer": "D", "type": "single"},
];

// 第七部分：出料与脱气系统
const List<Map<String, dynamic>> questionsPart7 = [
  {"content": "LLDPE装置产品出料系统中，交叉切换阀的主要作用是（）。", "options": ["实现系统交替出料，使系统利用率最大", "调节产品熔融指数", "降低反应器压力", "过滤树脂杂质"], "answer": "A", "type": "single"},
  {"content": "LLDPE装置单系统手动排料流程中，物流的第一个设备是（）。", "options": ["产品罐", "PDS出料泵", "反应器", "循环气回收塔"], "answer": "C", "type": "single"},
  {"content": "LLDPE装置PDS系统备用输送气是（）。", "options": ["反应气", "氮气", "工厂风", "回收气"], "answer": "B", "type": "single"},
  {"content": "产品脱气仓顶部过滤器(1213-Y-5010)的主要作用是（）。", "options": ["增加物流压力", "分离烃类和氮气", "冷却物流温度", "拦截树脂颗粒，防止进入排放气回收系统"], "answer": "D", "type": "single"},
  {"content": "产品脱气仓中用于脱除树脂烃类的氮气流动方向是（）。", "options": ["从顶部进入，底部排出", "从中下部进入，顶部排出", "从侧面进入，顶部排出", "从侧面进入，底部排出"], "answer": "B", "type": "single"},
];

// 第八部分：膜回收与火炬系统
const List<Map<String, dynamic>> questionsPart8 = [
  {"content": "膜回收系统中，VOC膜分离器的渗透气与深冷系统重组分液态烃加热后汇合的物流最终进入（）。", "options": ["1213-C-5241", "1213-C-5202", "1213-C-5254", "1213-C-1008"], "answer": "B", "type": "single"},
  {"content": "高压集液罐1213-C-5210压力控制范围是（）MPa.G。", "options": ["0.5-1.5", "0.83-2.0", "1.0-2.5", "2.5-3.5"], "answer": "B", "type": "single"},
  {"content": "低压火炬罐底部低压蒸汽加热器的作用是将低压火炬罐温度控制在（）。", "options": ["10℃-20℃", "30℃-60℃", "70℃-80℃", "90℃-100℃"], "answer": "B", "type": "single"},
];

// 第九部分：催化剂系统
const List<Map<String, dynamic>> questionsPart9 = [
  {"content": "BMC淤浆进料泵的循环模式中，浆料催化剂的流向是（）。", "options": ["从BMC淤浆进料罐到反应器", "从BMC淤浆进料罐到BMC淤浆进料泵再回到BMC淤浆进料罐", "从BMC浆料催化剂装运罐到BMC淤浆进料罐", "从BMC淤浆进料泵到TRIM进料罐"], "answer": "B", "type": "single"},
  {"content": "三乙基铝的闪点为（）。", "options": ["0℃", "-35℃", "-53℃", "53℃"], "answer": "C", "type": "single"},
  {"content": "T2系统（输送三乙基铝）操作时不需要穿烷基铝防护服。", "options": ["对", "错", "", ""], "answer": "B", "type": "judge"},
];

// 第十部分：造粒系统
const List<Map<String, dynamic>> questionsPart10 = [
  {"content": "造粒系统脱气仓回收氮气的主要来源是（）。", "options": ["深冷分离回收撬块的常温气体与氮气", "原料精制系统的新鲜氮气", "循环气压缩机的出口循环气", "挤压机的尾气"], "answer": "A", "type": "single"},
  {"content": "造粒系统种子床粉料的输送设备是（）。", "options": ["脱气仓风机K-5009", "膨胀机KT-5255", "循环气压缩机K-4001", "粉料树脂输送压缩机K-5613/5614"], "answer": "D", "type": "single"},
  {"content": "造粒系统拉料过程中，用于防止熔融泵轴承干摩擦的物流作用是（）。", "options": ["在熔融泵轴承间隙内充入树脂起润滑作用", "模孔充填以防止水进入模孔", "提高模孔的开孔率", "拉出被污染的树脂"], "answer": "A", "type": "single"},
  {"content": "挤压造粒机组是从（）公司引进的。", "options": ["美国杜邦", "日本日立", "德国科倍隆", "法国道达尔"], "answer": "C", "type": "single"},
];

// 第十一部分：风送系统
const List<Map<String, dynamic>> questionsPart11 = [
  {"content": "风送系统中，氮气介质的主要作用是（）。", "options": ["为LLDPE粉料输送提供气流动力", "冷却造粒后的高温颗粒", "终止反应器内的聚合反应", "去除颗粒中的残留催化剂"], "answer": "A", "type": "single"},
  {"content": "风送系统中，均化管线的主要作用是（）。", "options": ["增加颗粒的堆积密度", "将氮气介质冷却后循环使用", "储存暂时无法输送的颗粒", "将仓内各个时间段生产聚乙烯粒料均化均匀"], "answer": "D", "type": "single"},
  {"content": "LLDPE风送单元输送风机出口压力的正常控制范围是（）。", "options": ["0.2-0.4MPa", "0.1-0.2MPa", "0.4-0.6MPa", "0.6-0.8MPa"], "answer": "B", "type": "single"},
];

// 第十二部分：公用工程
const List<Map<String, dynamic>> questionsPart12 = [
  {"content": "HPS、LPS管线设置疏水器的主要作用是（）。", "options": ["排除管线内冷凝水", "调节管线压力", "过滤水中杂质", "输送高温介质"], "answer": "A", "type": "single"},
  {"content": "造粒单元引入循环水的主要作用是（）。", "options": ["吹扫工艺管线", "冲洗切粒机模板", "配制颗粒水", "供各换热器冷却使用"], "answer": "D", "type": "single"},
  {"content": "造粒单元引入生产水的主要作用是（）。", "options": ["清洗混炼机", "作为聚合反应原料", "冷却熔融泵", "满足单元内公用工程用水需求"], "answer": "D", "type": "single"},
];

// 第十三部分：工艺指标
const List<Map<String, dynamic>> questionsPart13 = [
  {"content": "LLDPE装置中氢气分子量调节剂的纯度控制指标为（）。", "options": ["≥99%", "≥99.5%", "≥99.9%", "≥99.99%"], "answer": "C", "type": "single"},
  {"content": "LLDPE装置中J催化剂浆液的固含量控制范围通常为（）。", "options": ["5-10%", "10-15%", "15-20%", "25-30%"], "answer": "C", "type": "single"},
  {"content": "LLDPE装置中乙烯进料的温度控制指标通常为（）。", "options": ["0-10℃", "10-20℃", "20-30℃", "30-40℃"], "answer": "C", "type": "single"},
  {"content": "LLDPE装置润滑油温度的正常控制范围是（）。", "options": ["30-40℃", "40-55℃", "55-65℃", "65-75℃"], "answer": "B", "type": "single"},
  {"content": "LLDPE装置冷却水系统的正常压力范围通常是（）。", "options": ["0.1-0.2MPa", "0.3-0.5MPa", "0.6-0.8MPa", "0.8-1.0MPa"], "answer": "B", "type": "single"},
];

// 第十四部分：安全与环保
const List<Map<String, dynamic>> questionsPart14 = [
  {"content": "炼油化工企业制定的生产安全事故应急救援预案，应当向（）备案。", "options": ["县级以上人民政府应急管理部门", "上级企业安全管理部门", "所在地消防救援机构", "行业主管部门"], "answer": "A", "type": "single"},
  {"content": "《安全生产法》规定，炼油化工企业的主要负责人对本单位安全生产工作负有的首要职责是（）。", "options": ["组织开展安全生产教育培训", "保证安全生产投入的有效实施", "组织制定并实施安全生产规章制度", "建立健全并落实本单位全员安全生产责任制"], "answer": "D", "type": "single"},
  {"content": "炼油化工中氮气对人体的最主要危害是（）。", "options": ["窒息性危害", "毒性腐蚀性危害", "易燃易爆性危害", "放射性危害"], "answer": "A", "type": "single"},
  {"content": "炼油化工中，氢气最显著的物理性质是（）。", "options": ["在标准状况下密度比空气小得多", "易溶于水", "沸点高于常温", "熔点高于0℃"], "answer": "A", "type": "single"},
  {"content": "炼油化工现场检测氢气泄漏最可靠的工具是（）。", "options": ["酚酞试纸", "可燃气体检测仪", "pH试纸", "酒精测试仪"], "answer": "B", "type": "single"},
  {"content": "皮肤接触三乙基铝时，正确的处理步骤是（）。", "options": ["用汽油或酒精擦去毒物后大量清水冲洗15分钟就医", "用肥皂水彻底冲洗", "直接用流动清水冲洗", "用碱水冲洗"], "answer": "A", "type": "single"},
];

// 第十五部分：设备知识
const List<Map<String, dynamic>> questionsPart15 = [
  {"content": "离心泵中用于防止泵内液体向外界泄漏的关键部件是（）。", "options": ["联轴器", "叶轮", "泵轴", "机械密封"], "answer": "D", "type": "single"},
  {"content": "离心泵的主要工作原理是通过叶轮旋转产生（）来输送液体。", "options": ["拉力", "向心力", "推力", "离心力"], "answer": "D", "type": "single"},
  {"content": "GSB-L2型立式高速泵的类型属于（）。", "options": ["容积式齿轮泵", "多级离心油泵", "单级单吸部分流离心泵", "往复式隔膜泵"], "answer": "C", "type": "single"},
  {"content": "用高速泵处理丁烯-1介质时，作业人员需穿戴（）。", "options": ["橡胶围裙", "普通工作服", "棉布手套", "防静电服"], "answer": "D", "type": "single"},
  {"content": "齿轮泵的主要作用是对熔融树脂进行（）。", "options": ["增压", "冷却", "加热", "过滤"], "answer": "A", "type": "single"},
];

// 合并所有题目
final List<Map<String, dynamic>> allQuestions = [
  ...questionsPart1,
  ...questionsPart2,
  ...questionsPart3,
  ...questionsPart4,
  ...questionsPart5,
  ...questionsPart6,
  ...questionsPart7,
  ...questionsPart8,
  ...questionsPart9,
  ...questionsPart10,
  ...questionsPart11,
  ...questionsPart12,
  ...questionsPart13,
  ...questionsPart14,
  ...questionsPart15,
];

// 获取完整题库
List<Map<String, dynamic>> getAllQuestions() {
  return allQuestions;
}

// 获取题库统计
Map<String, dynamic> getQuestionBankStats() {
  int single = allQuestions.where((q) => q['type'] == 'single').length;
  int multiple = allQuestions.where((q) => q['type'] == 'multiple').length;
  int judge = allQuestions.where((q) => q['type'] == 'judge').length;
  
  return {
    'total': allQuestions.length,
    'single': single,
    'multiple': multiple,
    'judge': judge,
  };
}
