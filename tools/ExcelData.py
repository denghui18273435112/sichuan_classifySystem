import xlrd
from configs.path import *
import json

def ExcelData(beginColumn=None,file_name="四川分类系统用例.xls"):
    """
    读取表格中的用例信息
    :param beginColumn:第一列的名称，支持模糊
    :return: 返回的数据格式字典

    表格字段说明
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
    """
    # excel_file=data_path+os.sep+file_name
    _data=[]
    #print(file_path_01)
    workbook = xlrd.open_workbook(file_path_01,formatting_info=True)
    sheets = workbook.sheet_names()
    for i in range(workbook.nsheets):
        sheet = workbook.sheet_by_name(sheets[i])
        title = sheet.row_values(0)
        for col in range(1,sheet.nrows):
            col_value = sheet.row_values(col)
            if beginColumn !=None:
                if beginColumn in sheet.cell(col,0).value:
                    _data.append(dict(zip(title, col_value)))
            else:
                    _data.append(dict(zip(title, col_value)))
    return _data


if __name__ == "__main__":
    print(ExcelData("case_PD_01"))




