@echo off
echo Testing Personal Finance Application...
java -cp build\classes\java\main;build\resources\main;gradle\wrapper\gradle-wrapper.jar;%USERPROFILE%\.gradle\caches\modules-2\files-2.1\com.fasterxml.jackson.core\jackson-databind\2.16.1\*;%USERPROFILE%\.gradle\caches\modules-2\files-2.1\org.slf4j\slf4j-api\2.0.9\*;%USERPROFILE%\.gradle\caches\modules-2\files-2.1\ch.qos.logback\logback-classic\1.4.14\* com.enterprise.personalfinance.PersonalFinanceApplication
pause
