class caseCheck:

    def case_Check(self,res=None):
        """
        校验实际结果与预期结果；预期结果肯定包含实际结果
        :param res:
        :return:
        """
        try:
            response_expect_result = res["response_expect_result"]
            actual_result = res["actual_result"]
            for key in response_expect_result:
                if (key in actual_result) & (actual_result[key]==response_expect_result[key]):
                    assert  True==True,"通过"
                else:
                    assert  True==False,"此用例校验失败.....;实际和预期结果未存在包含"
        except Exception as ERROR_NEW:
            raise  ERROR_NEW