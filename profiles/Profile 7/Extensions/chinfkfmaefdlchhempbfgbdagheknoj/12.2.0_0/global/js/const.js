const strConstExtensionId=browser.runtime.id,objConstExtensionManifest=browser.runtime.getManifest(),strConstExtensionName=objConstExtensionManifest.name,strConstExtensionVersion=objConstExtensionManifest.version,boolConstIsBowserAvailable="object"==typeof bowser,strConstChromeVersion=boolConstIsBowserAvailable?bowser.chromeVersion:"",boolConstUseOptionsUi=boolConstIsBowserAvailable&&strConstChromeVersion>="40.0"&&"Opera"!==bowser.name,strConstLogOnInstalled="browser.runtime.onInstalled",strConstDisabledDomainsSetting="arrDisabledDomains",strConstDisabledUrlsSetting="arrDisabledUrls",objConstUserSetUp="object"==typeof bowser?{currentVersion:strConstExtensionVersion,browserName:bowser.name,browserVersion:bowser.version,browserVersionFull:bowser.versionFull,chromeVersion:strConstChromeVersion,chromeVersionFull:bowser.chromeVersionFull,userAgent:bowser.userAgent,language:""}:{};"undefined"==typeof sttb&&(window.sttb={});const StorageApi=browser.storage,StorageSync=StorageApi.sync,StorageLocal=StorageApi.local;