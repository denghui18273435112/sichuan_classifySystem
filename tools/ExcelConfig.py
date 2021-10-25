class DataConfig:
    """
    主要的作用用于取表格某字段的数据
    #定义列属性
    #用例ID	模块	接口名称	请求URL	前置条件	请求类型	请求参数类型
    #请求参数	预期结果	实际结果	备注	是否运行	headers	cookies	status_code	数据库验证
    #用例ID
    """

    case_id = "用例ID"
    case_model = "模块"
    case_name = "接口名称"
    priority = "优先级"
    title = "标题"
    url = "请求URL"
    pre_exec = "前置条件"
    method = "请求方法"
    params_type = "请求头"
    params = "请求参数"
    expect_result = "预期结果"
    response_expect_result = "响应预期结果"
    actual_result = "实际结果"