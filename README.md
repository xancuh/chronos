<div align="center">
  <p>
    <h1>Chronos</h1>
    Chronos is a revival based off of the ECS source, but with a little modified changes to it. This will be the most detailed tutorial on how to host Chronos on your computer or VPS from the start to publishing a whole Roblox revival with rendering.
  </p>
</div>

> [!NOTE]
> You may use this source to learn and privately host your source to friends or to a small community. We do not recommend hosting this publicly.

## Dependencies:

Node.js: ```https://nodejs.org/dist/v18.16.1/node-v18.16.1-x64.msi```

PostgreSQL: ```https://sbp.enterprisedb.com/getfile.jsp?fileid=1258627```

.NET 6: ```https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/sdk-6.0.412-windows-x64-installer```

Go: ```https://go.dev/dl/go1.20.6.windows-amd64.msi```

# Setup

Download the source from Releases.

Install all of the dependencies, run them. When installing PostgreSQL, make sure to remember the credentials you set in the setup. This will be used in the next part.

Create a PG user, DB, and open pgAdmin 4. Start up everything, open ```config.json``` in services/api and put your credentials in there.

Install nodejs, go (lang), and dotnet 6. go into the services/api directory in a terminal, run "npm i", then run "npx knex migrate:latest".

Go into the services/Roblox/Roblox.Website folder and open "appsettings.json". Put in your DB info and any other configurable things. Also make sure to edit the "Directories" stuff (change "C:/Users/Administrator/Downloads/Chronos/services..." to the exact path of the unzipped source code, i.e. the path this README file is in by using Ctrl+H). Make sure to change every single auth string to your custom one. Remember these since they are useful in the future parts.

Go into the "services/Roblox/Roblox.Website" folder in a terminal, and run "dotnet run --configuration Release". If everything is successful, you should be able to visit the site at "http://localhost:5000/".

Start up the "admin" service by opening a new terminal, going into the "services/admin" folder, and running "npm i" then "npm run dev".

Open "services/2016-roblox-main/config.json" and replace ```https://chrns.vip/``` to your domain or ```http://localhost:5000/```. If you are using your domain, then please use ```https://your.domain/``` for the items and stuff to work properly.

Register an account, then go to"http://localhost:5000/admin/" and create 2 new accounts: ```UGC``` with any password with the ID of **2**. Go to "Players" and select UGC and "Nullify Password". Then create a new account named ```BadDecisions``` with any password with the id of **12** and nullify the password again.

In order to upload things, you will have to start up the "asset validation service". You can do this by going into "services/AssetValidationServiceV2" in a terminal and running "go run main.go".

Go to "services/game-server" and edit config.json to this:
```
{
    "rcc": "C:\\Users\\your-username\\Downloads\\Chronos\\services\\RCCService\\",
    "authorization": "enter render auth here from appsettings.json",
    "baseUrl": "http://localhost:5000",
    "rccPort": 64989,
    "port": 3040,
    "websiteBotAuth": "enter bot auth here from appsettings.json",
    "thumbnailWebsocketPort": 3189,
    "dockerDisabled": true
}
```

10. Go to "services/game-server" in a new terminal, and run "npm i", then "npm run build".

11. Close every running command prompt tab and run ```runall.bat``` in the services folder.

When you're done, it should open 5 command prompts and nothing else and enjoy!

# Common fixes:

Below are common fixes to known issues with this source. This applies with any other ECS source.

## Application still pending:
```
[HttpGet("/acceptapp")]
        public async Task<dynamic> acceptapp()
        {
            await services.users.ProcessApplication("your-application-id-from-the-site", 1, UserApplicationStatus.Approved);
            return new { };
        }
```
You must go to "services/Roblox/Roblox.Website/Controllers/Internal" and open "BypassController.cs" and place it anywhere (near below the script).
Next, you must restart the command prompt that is running ```dotnet run```. To do this, do CTRL+C then type in the same command. After, visit ```/acceptapp``` on the auth/application page to accept the app instantly!

## Roblox Main UI not loading:

This is simple. Edit the ```config.json``` in "services/2016-roblox-main" to match your localhost domain instead of your actual domain. For example: 
```"baseUrl":"https://localhost:3000/","apiFormat":"https://localhost:3000/apisite/{0}{1}"```
You may also use ```localhost:5000``` but I recommend the port ```:3000```.

## Game-server error (MODULE_NOT_FOUND)

Go to the game-server command prompt (where it's running the game-servers) and run ```npm install @types/node@latest typescript@latest```.

After it is finished, delete the ```node_modules``` folder andd then go to ```tsconfig.json``` and replace everything with the below text:
```
{
  "compilerOptions": {
    "baseUrl": ".",
    "outDir": "./dist",
    "target": "es2022",
    "lib": [
      "es2022",
      "dom",
      "esnext.disposable"
    ],
    "typeRoots": [
      "./node_modules/@types"
    ],
    "noImplicitAny": true,
    "noImplicitThis": true,
    "strictNullChecks": true,
    "strictBindCallApply": true,
    "strictFunctionTypes": true,
    "module": "commonjs",
    "moduleResolution": "node",
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    "sourceMap": true,
    "declaration": false,
    "allowSyntheticDefaultImports": false,
    "strict": false
  },
  "include": [
    "./src/**/*.ts"
  ],
  "exclude": [
    "node_modules",
    "./public",
    "www/dist",
    "test"
  ]
}
```
This is a new tsconfig.json because the old config uses es2016, which has packages that aren't available for es2016. This uses es2022. More reliable and has support for esnext.disposable and even more.

After you've pasted that, save it and then do ```npm i``` and finally you should be able to do ```npm run build``` & ```npm run start``` if you've followed the fix accordingly.
