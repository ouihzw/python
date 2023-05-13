# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import settingWebCookieObjectSettingDialog
from ...webPageOperationConstants import WebPageOperationConstants

class SettingWebCookieFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(SettingWebCookieFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebPageOperationConstants.settingWebCookieDirective
        self.directive["data"] = {"setting_mode": 0,
                                  "web_object": "",
                                  "browser_type": 0,
                                  "cookie_url": "",
                                  "cookie_name": "",
                                  "cookie_value": "",
                                  "cookie_domain": "",
                                  "cookie_path": "",
                                  "https_only": False,
                                  "secure": False,
                                  "session_cookie": True,
                                  "cookie_expiration_date": "100",
                                  "log": True,
                                  "handle": 0,
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = settingWebCookieObjectSettingDialog.SettingWebCookieObjectSettingDialog(self.title,self.directive["_id"], self.id)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.urlSettingModeCombobox.setCurrentIndex(data["setting_mode"])
        self.settingDialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.cookieUrlLineEdit.setText(data["cookie_url"])
        self.settingDialog.cookieNameLineEdit.setText(data["cookie_name"])
        self.settingDialog.cookieValueTextEdit.setText(data["cookie_value"])
        self.settingDialog.cookieDomainLineEdit.setText(data["cookie_domain"])
        self.settingDialog.cookiePathLineEdit.setText(data["cookie_path"])
        self.settingDialog.markedAsHttpOnlyCheckbox.setChecked(data["https_only"])
        self.settingDialog.markedAsSecureCheckbox.setChecked(data["secure"])
        self.settingDialog.setToSessionCookieCheckbox.setChecked(data["session_cookie"])
        self.settingDialog.cookieExpirationDateLineEdit.setText(data["cookie_expiration_date"])
        self.settingDialog.printErrorLogsCheckbox.setChecked(data["log"])
        self.settingDialog.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.settingDialog.retryCountSpinbox.setValue(data["retry_count"])
        self.settingDialog.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["setting_mode"] = self.settingDialog.urlSettingModeCombobox.currentIndex()
        data["web_object"] = self.settingDialog.webObjectCombobox.currentText()
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["cookie_url"] = self.settingDialog.cookieUrlLineEdit.text()
        data["cookie_name"] = self.settingDialog.cookieNameLineEdit.text()
        data["cookie_value"] = self.settingDialog.cookieValueTextEdit.toPlainText()
        data["cookie_domain"] = self.settingDialog.cookieDomainLineEdit.text()
        data["cookie_path"] = self.settingDialog.cookiePathLineEdit.text()
        data["https_only"] = self.settingDialog.markedAsHttpOnlyCheckbox.isChecked()
        data["secure"] = self.settingDialog.markedAsSecureCheckbox.isChecked()
        data["session_cookie"] = self.settingDialog.setToSessionCookieCheckbox.isChecked()
        data["cookie_expiration_date"] = self.settingDialog.cookieExpirationDateLineEdit.text()
        data["log"] = self.settingDialog.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.settingDialog.handleErrorWayCombobox.currentIndex()
        data["retry_count"] = self.settingDialog.retryCountSpinbox.value()
        data["retry_interval"] = self.settingDialog.retryIntervalSpinbox.value()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        if data["setting_mode"] == 0 and data["session_cookie"] is True:
            self.infoFormat = u"设置会话cookie，url:网页对象%s 名称:%s、值:%s、域名:%s、路径:%s、httpOnly:%s、secure:%s"
            super().updateSecondLineInfo(("${" + data["web_object"] + "}", data["cookie_name"], data["cookie_value"],
                                          data["cookie_domain"], data["cookie_path"], str(data["https_only"]),
                                          str(data["secure"])))
        elif data["setting_mode"] == 0 and data["session_cookie"] is False:
            self.infoFormat = u"设置有效期为%s的持久性cookie，url:网页对象%s 名称:%s、值:%s、域名:%s、路径:%s、httpOnly:%s、secure:%s"
            super().updateSecondLineInfo(
                (data["cookie_expiration_date"],"${" + data["web_object"] + "}", data["cookie_name"], data["cookie_value"],
                 data["cookie_domain"], data["cookie_path"], str(data["https_only"]), str(data["secure"])))
        elif data["setting_mode"] == 1 and data["session_cookie"] is True:
            self.infoFormat = u"设置会话cookie，url:%s 名称:%s、值:%s、域名:%s、路径:%s、httpOnly:%s、secure:%s"
            super().updateSecondLineInfo(
                (data["cookie_url"], data["cookie_name"], data["cookie_value"],
                 data["cookie_domain"], data["cookie_path"], str(data["https_only"]), str(data["secure"])))
        elif data["setting_mode"] == 1 and data["session_cookie"] is False:
            self.infoFormat = u"设置有效期为%s的持久性cookie，url:%s 名称:%s、值:%s、域名:%s、路径:%s、httpOnly:%s、secure:%s"
            super().updateSecondLineInfo(
                (data["cookie_expiration_date"],data["cookie_url"], data["cookie_name"], data["cookie_value"],
                 data["cookie_domain"], data["cookie_path"], str(data["https_only"]), str(data["secure"])))
