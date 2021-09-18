## Important notes  

#### If anyone ends up using this, do shoot me a message and let me know how it's working for you! I would love to hear.
#### Current version works - minus the WordPress integration. I believe something changed with one of the required plugins. I have not had a chance to test it yet. For now, in the config, for "wordpress" enter "no".

#### I will try and turn the actual docs into a real wiki page on here. 
----
# Welcome to the Verifier documentation page
# Features
Reduce Asset Piracy  
Self-service asset verification  
Multi asset verification  
Multi publisher account  
Self-hosted (Can even be hosted on home server / desktop PC)  
Hosting can be provided if need be.

* Eliminate the need to manually verify customer asset invoices. Allows asset developers to have private/locked channels in their Discord server in which only verified customers have access.
* By only providing support within channels that require verification of ownership you will be helping to reduce the risk and effects of piracy of your asset. No proof of purchase, no support.
* As an additional benefit to your customers, you can safely offer secure links to critical updates of your asset without having to wait for Asset Store approval while maintaining peace of mind, as only verified purchasers will be able to view / download the content.

* Verification is a quick and easy process for the customer and relieves the bordon of having to manually verify past or future customers. They simply submit their invoice number, the invoice is verified, the customers Discord account is then granted permission to the appropriate channel(s).
* It features multi asset verification and individual permission per asset which allows you to only give access to channels specific to each asset. Though, this is optional. 
* Verification of a single asset can grant permission to all channels if you wish. If your assets are split between more than one publisher account, that is not a problem.

 Ex. 1 If you have one asset:  
* Verification could unlock access to a support, downloads, and feature-suggestion channel

Ex. 2 If you have three assets:  
* Verification of asset 1. could unlock access to a Asset1-support(specific to asset 1), Asset1-downloads(specific to asset 1), and a general feature-suggestion channel.  
* Verification of asset 2. could then also unlock access to asset2-support and asset2-downloads while maintaining access to the general feature-suggestion channel.  
* Verification of asset 3. could then unlock access to asset3-support, asset3-downloads, asset3-beta, and a asset3-beta-news channels.  


Once an invoice number is verified and claimed it is then tied to the users account and saved to your choice od database. This eliminates the risk of an invoice number sharing between multiple people/accounts. 
	Database lookup tools are provided (currently invoice and username) and are able to be accessed directly through Discord, no need to log onto the server to go searching for information.
				
				
### **Additional features and tools will be added. Suggestions are always welcome!**
# Prerequisites
   Requirements: Depending on your host operating system as well as what features you plan to use while determine what additional items are requires.

   If using MS SQL Server (Azure SQL) - You will need the SQL Server ODBC Driver installed on the machine Verifier will be running. Otherwise, you can just use the included local database, or MySQL.

[Download MS SQL ODBC Driver 17](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-2017)
 
# Installation Steps
The order of operation to get Verifier up and running is as follows:
 
**1. Prepare Discord:**
 * Determine how you would like things to actually operate. Do you have a single asset and would like 3 locked channels? Do you have multiple assets and you want each one verified individually and different channels for each asset?
	 * **If you just have one asset** and want verification of that asset to grant access to a few locked channels:
		 *  Create a role within the server settings of Discord by clicking on the drop down menu above your servers name and select "Server Settings" and then fine the  "Roles" menu tab. There is a little plus(+) symbol you can press in order to create a new role. Typically naming the role "Verified" is common practice as it is easy to tell what it is for. 
		 * If you right click in the channels area you can create a channel category and set it to private and the select your "Verfied" role. Any channels you create in this private category will automatically inherit the permissions of the category.
		 * Next create the channels you wish to have, such as "Support", "Downloads", or whatever you wish, if they are made in a private category they should have the permissions applied, but if you decide you do not want the channels all to be within the same category you can make the channel anywhere, you just have to make sure you turn on the "Private Channel" option when creating the channel, this will remove the base general permissions from the start.
		 * Once "Private Channel" is selected it will allow you to add your newly created role to the channels and this will give the "Text Permissions" to the channel, such as ability to read messages (present and past) and give the ability to chat in the channels.

	 * **If you have multiple assets** and would like individual permissions and channels per asset:
		 * The steps for this are similar to the ones above except you will want to create the "Verified" role, but then also create a role with a name corresponding to each asset. 
			 * ex. If you have 2 assets (My Asset 1 and My Asset 2) make one "Verified" role and then one role for each asset such as (asset1 and asset2)
		 * It is ideal to create a category for each asset and only apply the role that is specific to that asset to the category. ex. If the category is for asset1, do not apply the "Verified" role as well as the role of asset1, only apply asset1 role. This is because anyone who verifies ownership of any asset will get the "Verified" role as well as the role for the asset they verified. This is to allow for shared channels for anyone who is a purchaser of at least one of your assets but then also specific support or download channels.
		 * Once you have your channels and roles setup how you would like them, move on to step 2.

**2. Follow the steps in this link to [Enable Developer Mode](#enabledev).**

**3. Follow the steps in this link to [Obtain Id numbers for settings](#obtainid). You will need the ID number for your server itself as well as the ID number for each of your roles. You may want to create a text file and save each one in there as you obtain them just to make things easier. That is your call, of course.**

**4. Once you have the ID for your server, the "Verified" role, and if you have multiple assets,  the ID for each of the asset specific roles you will need to fill in the configuration files. Proceed to the [Configuration](#configuration) section below.**

**5. Once config.json and dbconfig.json are filled out it depends on if you are going to be using the WordPress integration whether that needs to be filled out or not. If so, please see the [WordPress](#wordpress) section. Otherwise you can move on.**

6. The next step will be starting up Verifier. Depending on if you are running on Linux or Windows. it will either be a binary file called "Verifier" or "Verifier.exe" respectively.**  
**6. EDIT (I originally intended on this being a compiled application, which it could be still as I have included the setup file and .spec files to compile with pyinstaller, but it is suffecient to simply run ```python3 __main__.py``` from the root directory once the configs are setup. (must be python 3.7))**

**7. Once Verifier has started up you will be greeted with a link in the console window. Clicking this link will bring up your browser and take you to a Discord page which has you select your server so that it is allowed to join.**

**8. At this point you should have Verifier up and running in your server under the name in which you gave it when creating the bot application through the Discord developer portal.**

**9. The next step is to setup the database. Begin a private message directly with the bot. If you left the `commandprefix` field default you will type in `!cmddbsetup`. This will automatically create the tables Verifier requires either in the internal database or using one of the other options if you set them up.**

**10. If you are integrating WordPress you will need to now connect Verifier to WordPress by following [these final steps](#finalsteps). Otherwise, you should be good to go!**

Please reference the command list at the end of this document.

----

 <a name="configuration"></a>
# Configuation
----

There are a few configuration files that need to be filled out that you will find in the /config/ folder. The first one being config.json. 

Included are a default-config.json, default-dbconfig.json, and default-wordpress.json,  as well as an example of each named with example-\*.json which has fake information 
filled out in case you want to see how a config would look.  The below sections have the detailed information.

Do not change the information within the files prefixed with "default-", you must make a copy each of the files with the "default" prefix and remove the "default-" text from the name so that they are name as follows:  config.json, dbconfig.json, 
and wordpress.json. They will not be seen by Verifier unless they are named as just stated. This is required so your actual config files are not overwritten during an update. 

We will start by filling out config.json

 <a name="config"></a>
 ## config.json
**token** - Discord Authentication Token from [https://discordapp.com/developers/applications/](https://discordapp.com/developers/applications/)
1. You will need to go to the link above, which (when logged in) will take you to the developer section of Discord. 
2. Here you will need to click on the "Create an application button". You will need to fill out the name of your bot.  
![https://i.imgur.com/mYnqd69.png](https://i.imgur.com/mYnqd69.png)

3. Once that is completed you will want to click on the "Bot" tab on the left side menu. From there you will need to click on the "Add Bot" button to turn the newly created application into a bot.  
![https://i.imgur.com/k3ya1kQ.png](https://i.imgur.com/k3ya1kQ.png)

4. From there the "Click to Reveal Token" text will be displayed. Once you click that it will give you a text string. This will be pasted into the first property of the config.json.  
![https://i.imgur.com/12RIZuV.png](https://i.imgur.com/12RIZuV.png)

**miscsettings - requireemail**
*(This setting is required when using the [WordPress](#wordpress) integration, as it is how it will locate the users account but can also be used without the integration)* 

* This setting will require the user to input their email address before being able to verify their asset. The email address will be stored in Verifier's database along with their Discord username. 

**commandprefix**
* Command prefix is the character string you will type to your bot in order to signify the beginning of a command statement in which the bot will listen / respond  
ex. If your command prefix is "!cmd" and you want to send Verifier the command "hellobot" your statement to the bot would appear as this "!cmdhellobot"

**discordIds - guild**
Guild is the identification number for the server itself. You should have this from step #3 of the installation steps. If not here is how you obtain it:
* While in your server, Click on the dropdown arrow next to your server name near the top left of your Discord window while you are in your servers main window.
Locate and click the "Server Settings" text.
In the left side menu locate and click the "Widget" tab. 
Copy the text in the "Server ID" box and paste that value into the config files `guild: PasteGuildID` property but without any quotes. All numeric only values are counted as integrer values in Verifier and must not be in quotes. I will make a note that in an update I will change this so that it will work either way.

**discordIds - botusers (Optional)**

* 'botusers' is a role you can give trusted members such as other admins or moderators. This role must be manually created and then added to the individual members you would like to be able to access additional features.
Note that it will give them ability to query and delete stored user information. It is not required that this role be given to anyone.

**roles (Please see the "Developer Mode" section of the documentation titled "Obtain Id numbers for settings" under the "Explanations" heading on how to obtain the "roles" Id number.)** 
* (Important) - This is where you will put in the role ID's you obtained from step #3.  While the names of the roles within Discord do not matter, they do matter in the config file. In the example below "Verified", "asset1", and "asset2" are names(referred to as [shortcodes](#shortcodes)) that need to match up with their corresponding asset settings in the "apiKeys" and "packages" near the end of config.json (as well as in wordpress.json if using the WordPress integration). Please see the "[Shortcode](#shortcodes)" section of the documentation under the "Explanations" heading.) 
* **Verified** - 'Verified" is the generic verified ID. It can be used if you only have 1 asset or as a general "verified" role  to allow access to multiple channels not specific to a single asset (ex. general support, news, update info, etc)
  
Example roles section:
(shortcode: RoleIdNumber)
```    
  roles:{
    Verified:   1234567890123456,
    asset1:     2345678901234567,
    asset2:     3456789012345678,
  },
```
  
**datecompare** (If not using, leave set to "No")
Date compare is used if you depreciated one asset and came out with another in it's place of the same name.  
ex. asset1 is version 1 of your asset vs asset2 is version 2 of your asset but both are named "My Awesome Asset" on the Asset Store. You set this to "Yes" and then fill in the date in the "comparedate" field with the date that Unity made the switchover.
 
 **comparedate**
Compare date is the date in which your new asset took over from your old one to determine which one is being verified against.  
  `comparedate: "2018-12-24",` (Format is Year-Month-day)

**compareasset1** **compareasset2**
If you are comparing two assets to determine which to verify put the earlier released asset's shortcode(link) as compareasset1  
If the customers purchase date is more recent than your compare date, they are verified for the newer asset (compareasset2)  
  `compareasset1: "asset1",`  (Shortcode(link) of original asset)  
  `compareasset2: "asset2",`  (Shortcode(link) of newer asset)
  
**apiKey**   
**package**
Here is where you will put the shortcode(link) of your asset along with the publisher API key(s) and in the second section
you will have your shortcode(link) along with the string name of your asset exactly as it is in the asset store.  

```
  Format
  apiKey -  shortcode: "API Key",
  package - shortcode: "Name of asset as set in Asset Store",

  apiKey:{
    asset1: "ThisIsMyApiKey123",
  },
  package:{
    asset1: "This is: My Awesome Asset 1",
  }
```
----
 <a name="dbconfig"></a>
## dbconfig.json
The default is a built in light weight json based database which requires no additional configuration other than leaving "Internal" typed into the "database" field.
The other options currently include "MySQL" and "Azure" (typing "Azure" will work for most any MS SQL Server)  

**database** Enter your choice of database type you would like to use.  
For internal database it would look like this. : `database: "Internal",`   
For MySQL database it would look like this. : `database: "MySQL",`  

The other options below only need to be changed / filled out if you are going to be using MySQL, or Azure (MS SQL Server) and are pretty self explanatory.  

  * **address**: "example.com", (Without http://, just the address.)  
  * **usename**: "myusername",  
  * **password**: "MyPassword1@",  
  * **dbname**: "database1",  
  * **dbprefix**: "", (If you would like to use a table prefix, please type it in here, otherwise leave the quotation marks empty.
   ex. If you type "verifier_" into the prefix the table names in the database will come out as `verifier_table_name` as opposed to just `table_name` )  
  * **charset** Chances are you will not need to modify the character set, but if you do, you can. If you don't know what it is or you are in doubt, just leave it as is.

----
 <a name="explanations"></a>
# Explanations
 <a name="roles"></a>
## Roles
When using Verifier you will create a role that signifies that a user has been verified and now has permission to enter a locked channel. 
You will then add that role to the channels you would like the user to then be able to enter.

Roles need to be manually created. A role is a set of permissions in which are granted to users. Roles are also used to permit access to channels that "locked" or "private".
   
If a channel is set to private roles then need to be manually added under that channels settings in the "permissions" tab.   
If a role is added to a channel you can then specify what users with that role are permitted to do in that channel.  
At a minimum the permission named "Read Messages" needs to be turned on in order for someone with the given role to be able to enter that channel.
    
From there you can specify to your liking what else they can do. If you wish for them only to be able to read things that someone with the ability to post has said 
(example being an 'Announcements' channel or 'News' in which you want it to be read only) then you can turn on only the "Read Messages" permission but you would probably also want to enable the "Read Message History" permission in order for the user to read past messages.

Some examples would be:

* Ex. 1.  
    * If you have one asset, you may have one "general-chat" channel which is set to the default permission to allow any user in so that new users to your channel who have not yet verified have a place to chat when they enter.  
    * You might also have another unlocked channel called "presale-questions" so that a user might be able to ask questions about your asset before they purchase it.  
    * You might also have 3 locked channels, such as "support", "downloads", and "feature-suggestions" and then a single role called "Verified". 
    * You go to the channel settings for each of the channels and set the @everyone permissions to none by disabling all of the permissions in the list. 
    * You then add the "Verified" role and drag it above the @everyone role and then enable the permissions you would like users who are verified to have. 
     (Typically this would be the permissions under the "Text Permissions" category only, not the "General Permissions". Those are usually reserved for  server Administrators / Moderators roles. Those permissions would be setup and applied separately.)
    * Once you have the permissions applied to the channel, Discord will now allow anyone with the role you added to be able to see and enter the channel.


* Ex. 2.  
    * If you have three assets, everything would be similar to example one except you might have a separate channel (or set of channels) for each of your assets. 
    * You have a role named asset1 which would be added to a channel named asset1-support(specific to asset 1), asset1-downloads(specific to asset 1), and a general feature-suggestion channel.
    * You have a role named asset2 which would be added to asset2-support and asset2-downloads while also giving access to the same general feature-suggestion channel as the asset1 role.
    * You have a role named asset3 which would be added to asset3-support, asset3-downloads, asset3-beta, and a asset3-beta-news channels.
    For the Ex. 2 scenario you would create a "Verified" role, but then also 3 other roles, one for each of your 3 assets. They can be named whatever you would like in Discord, the role Id number is what will matter to Verifier. 
    
Once you decide on many channels you would like and which roles you would like to be able to access which channels, 
you will need to follow the steps below to enable developer mode so you can get your new roles Id numbers so they can be input into the Verifier config files.

  
 
 ----
 <a name="enabledev"></a>
 ##  Enable developer mode 
Several settings in the configurations require you to enable developer mode in order to be able to get the values you need to enter. To enable developer mode, please follow the steps below.
1. In the bottom left area of Discord, to the right of your names display will be a cog wheel, click this.  
![https://i.imgur.com/XEhE277.png](https://i.imgur.com/XEhE277.png)

2. In the left side menu locate and click the "Appearance" tab.   
![https://i.imgur.com/7G2lwFF.png](https://i.imgur.com/7G2lwFF.png)

4. Scroll down to the "Advanced" section and toggle "Developer Mode" to on.  
![https://i.imgur.com/ID0xk2E.png](https://i.imgur.com/ID0xk2E.png)

 <a name="obtainid"></a>
## Obtain Id numbers for settings (botusers and roles)
1. Once developer mode is enabled (see above) you will be able to obtain the Id numbers for your roles. To accomplish this you will be to make sure the settings of "Allow anyone to @mention this role" is turned on (only long enough to obtain the Id, then it can be turned off).
2. Once the @everyone mention is turned on go into a chat channel and type the @ symbol, this will display a list of roles and users that can be @mentioned.
3. Find the role in which you need to obtain it's Id and select it. This will then have the roles name along with an @ in front of it in the chat's send box. Before you hit enter you will need to play a "\" before the @ symbol so that if, for example, your roles name is "asset1" the text in the chat box looks like this: ` \@asset1 `
4. You can then hit enter and it will send the text to the channel and then display the roles ID as seen below. You can then copy and paste this role Id into the appropriate field in the config file.  The ID number is the numeric values only, disregard the `@` and `&` symbols.  

![https://i.imgur.com/Paye23m.png](https://i.imgur.com/Paye23m.png)

5. To obtain the "guild id" (server id), go to the server settings menu and select the "Widget" menu option. There it will display the "Server ID" as seen below. This is the number that will go into config.json under the "guild" property.  

![https://i.imgur.com/1tdrySj.png](https://i.imgur.com/1tdrySj.png)

 <a name="shortcodes"></a>
## Shortcodes
Values that are referred to as "shortcodes" are simply acronyms or shorthand versions of your assets names that you will need to come up with name such as if your assets name is "Super Awesome Asset 2", your shortcode could be "SAA2".
It can be anything you like as long as it has no spaces or special characters but you must use the same shortcode in all 
places that require a shortcode to be input for your asset as that is what Verifier uses to reference the different settings and properties and tie them together.

The places that require shortcode entry are :  
    config.json under "roles"  
    config.json under "apiKeys"  
    config.json under "packages"  
    wordpress.son under "assets"  
    
Below is an example of how config.json and wordpress.json might look to show matching shortcodes, role ID numbers, API Key text, Asset name within the Asset Store, and WordPress role name
    
```
// config.json
  roles:{
// (shortcode: RoleIDNumber) (no quotes around number)
    Verified: 468710520002969600,
    asset1: 495402309912756242,
    asset2: 495402356612268035,
  },

  apiKey:{
// (shortcode: "API Key" )
    asset1: "ThisIsMyApiKey123",
    asset2: "ThisIsMyApiKey123",
  },
  package:{
// (shortcode: "Name of asset as set in Asset Store" )
    asset1: "This is: My Awesome Asset 1",
    asset2: "This is: My Awesome Asset 2",
  }
  
// wordpress.json
  assets:{
// (shortcode: "WordPressRoleName" )
    asset1:"asset1",
    asset2:"asset2",
  },
  
  
```

----------------------------------------------------------------------------------------------------------------------------------------

----
 <a name="commands"></a>
# Commands

All commands begin with the configured `commandprefix`. If you left it default than it is `!cmd` followed by one of the commands below. (Without a space.) Otherwise it will be whatever you set it as.

ex. `!cmdverify`

```
verify -        The first step in the validation process (suggested that this is the only command you advertise to users)
                Calling 'verify' prompts the bot to PM the user with instructions on how to proceed 

validate -      (For security purposes, this command should only be used in a private message with the Verifier bot.)
                This is the call that actually performs the validation process, it takes in 2 arguments. 
                The first is the shortcode(link) for the asset being verified. The second is the invoice number.
                                ex. !cmdvalidate asset1 1234567890

searchinvoice - This is an admin/moderator command that takes in 1 argument, the invoice number you would like to look up.
                If the invoice number exists in the local database it will return the username in which it is assigned

searchuser -    This is an admin/moderator command that takes in 1 argument, the username you would like to look up.
                If the user exists in the local database it will return a listing of the assets/invoice numbers assigned to the user.

deleteinvoice - Allows you to delete an individual invoice number from a users account. 

load -          Discord Assistant was built in a modular fashion and is extensible. Additional modules may be released 
                if there are requests for additional functionality. Modules can be added at runtime using '!cmdload modulename'
                to hot-load a new module directly from Discord

reload -        Primarily for development purposes allowing for quick iteration of testing changes by hot-reloading a module
                If you are making your own module for Verifier you can use !cmdreload modulename directly in Discord
                to test changes without having to restart the bot

purge_all -     Primarily used for development purposes. 'purge_all' will delete all messages in the current channel within the last 12 days

dbsetup -       This will automatically create the necessary tables in which Verifier requires to save its data when a user verifies their assets.

wpsetup -       This begins the connection between Verifier and your wordpress site via Oauth2.
```


![alt text](https://i.imgur.com/cg5ow2M.png "instance.id")
