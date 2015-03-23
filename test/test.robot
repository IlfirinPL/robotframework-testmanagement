*** Settings ***
Library           TestManagementLibrary
Library           OperatingSystem
Library           Screenshot

*** Test Cases ***
Test
    Connect To Rally    URL    USER    PASS    WORKSPACE    log_file=/tmp/rally.log
    Create File    test1.txt    example log
    Create Directory    pic
    Take Screenshot    ${EXECDIR}/pic/test2.jpg
    @{list}    Create List    test1.txt    ${EXECDIR}/pic/test2.jpg
    Add Test Result    TC5001    1230 DEV    Fail    tester=Tester    notes=Automated exectuion    attachment_list=${list}
