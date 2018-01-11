# Power BI REST API example + Python

This repository present a guide and some example code in Python to connect to Power BI API, and notably to generate and embedded token. The documentation is not exactly clear on the topic, and most of the examples are in C#. The whole thing is frankly quite confusing and poorly documented if you stray out of the C# path.

**tl;dr**: use `https://login.microsoftonline.com/common/oauth2/token` to generate the Access Token. Get your app permission right.

## Pre-requisite

You'll need:
- an Organizational Active Directory, and a global admin on it
- a PowerBI Pro Licence (you can get one for free, for trial)
- a user in your AD that is also logged in to Power BI

### Create an application

You need to create an application, follow this tutorial: https://docs.microsoft.com/en-us/power-bi/developer/register-app. Make sure you save the application secret and application id.

Make sure the permissions are all correct (remember you have to click "Save" then "Grant permissions" when modifying the permission in Azure AD).

### Create a PowerBI Workspace

Login to PowerBI with the user you want to own the workspace. It doesn't have to be an admin, but it needs access to Power BI. This user is the _master user_.

Create a new Workspace. The name doesn't matter. In that workspace, create a dashboard or a report.

Click on any report/dashboard, note the URL should be something like `https://app.powerbi.com/groups/{group_id}/reports/{report_id}/ReportSection`. Remember the group_id for testing purpose.


## Talking with the API

The API is [documented here](https://msdn.microsoft.com/en-us/library/mt147898.aspx), we show some example of accessing it.

### Generating an Access Token

First thing first, you need to generate an access token, that will be used to authenticate yourself in further communication with the API.

Endpoint: https://login.microsoftonline.com/common/oauth2/token
Method: POST
Data:
- grant_type: password
- scope: openid
- resource: https://analysis.windows.net/powerbi/api
- client_id: APPLICATION_ID
- client_secret: APPLICATION_SECRET
- username: USER_ID
- password: USER_PASSWORD

replace APPLICATION_ID, APPLICATION_SECRET with the application id and secret you got after creating the app in AAD. Replace USER_ID and USER_PASSWORD with the login/password for the master user. Leave the rest as is.

If successful, you should obtain a response similar to:

```json
{'access_token': 'eyJ0...ubUA',
 'expires_in': '3599',
 'expires_on': '1515663724',
 'ext_expires_in': '0',
 'id_token': 'eyJ0A...MCJ9.',
 'not_before': '1515659824',
 'refresh_token': 'AQABAA...hsSvCAA',
 'resource': 'https://analysis.windows.net/powerbi/api',
 'scope': 'Capacity.Read.All Capacity.ReadWrite.All Content.Create Dashboard.Read.All Dashboard.ReadWrite.All Data.Alter_Any Dataset.Read.All Dataset.ReadWrite.All Group.Read Group.Read.All Metadata.View_Any Report.Read.All Report.ReadWrite.All Tenant.Read.All Workspace.Read.All Workspace.ReadWrite.All',
 'token_type': 'Bearer'}
```

If you get a 403 error, your credentials are invalid, check your application id / secret and user id / secret.

### Using the API

Save the value `access_token` from the previous call, you'll need it here.

Endpoint: https://api.powerbi.com/v1.0/myorg/groups (for example, to get the list of groups)
Method: GET
Headers:
- Authorization: Bearer <token you saved before>
- Content-Type: application/json; charset=utf-8

Should return the list of Workspace you created.

Another example:

ENDPOINT: https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports replace group_id with the value saved earlier. Gets the list of reports available in a workspace.
Method: GET
Headers:
- Authorization: Bearer <token you saved before>
- Content-Type: application/json; charset=utf-8

Should return the list of reports in the workspace.


## Embedding a dashboard / report / ...

### Generating an embed token:

Endpoint: https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/GenerateToken replace group_id and report_id
Method: POST
Data: null
Headers:
- Authorization: Bearer <token you saved before>
- Content-Type: application/json; charset=utf-8

Should, on success, return something like:

```json
{'@odata.context': 'http://api.powerbi.com/v1.0/myorg/groups/.../$metadata#Microsoft.PowerBI.ServiceContracts.Api.V1.GenerateTokenResponse',
 'expiration': '2018-01-11T10:13:18Z',
 'token': 'H4sIAAAAAA...8T__C5gq8MEaCwAA',
 'tokenId': 'xxxxx'}
```

### Embedding a report in an HTML page

We can use the template provided at https://docs.microsoft.com/en-us/power-bi/developer/embed-sample-for-customers. The file `powerbi.js` can be found [here](https://github.com/Microsoft/PowerBI-JavaScript/blob/master/dist/powerbi.js) (and we removing the other dependency to some external library in that example).

```html
<script src="~/scripts/powerbi.js"></script>
<div id="reportContainer"></div>
<script>
    // Read embed application token from Model
    var accessToken = "EMBEDDED_TOKEN";

    // Read embed URL from Model
    var embedUrl = "EMBEDDED_URL";

    // Read report Id from Model
    var embedReportId = "REPORT_ID";

    // Get models. models contains enums that can be used.
    var models = window['powerbi-client'].models;

    // Embed configuration used to describe the what and how to embed.
    // This object is used when calling powerbi.embed.
    // This also includes settings and options such as filters.
    // You can find more information at https://github.com/Microsoft/PowerBI-JavaScript/wiki/Embed-Configuration-Details.
    var config = {
        type: 'report',
        tokenType: models.TokenType.Embed,
        accessToken: accessToken,
        embedUrl: embedUrl,
        id: embedReportId,
        permissions: models.Permissions.All,
        settings: {
            filterPaneEnabled: true,
            navContentPaneEnabled: true
        }
    };

    // Get a reference to the embedded report HTML element
    var reportContainer = document.getElementById('#reportContainer')[0];

    // Embed the report and display it within the div container.
    var report = powerbi.embed(reportContainer, config);
</script>
```

Replace the values:
- `EMBEDDED_TOKEN` with the token we just generated (NOT the access token)
- `EMBEDDED_URL`: an URL specific to your report. You can obtain it using the endpoint https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports
- `REPORT_ID` the id of your report.

## In Python

The file `example.py` shows Python example to access the API using the `requests` module (but no other dependency on Azure module!).


## Licence

MIT