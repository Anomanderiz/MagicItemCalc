# Magic Item Calculator

## Password protection

The app requires a bcrypt password hash in the `APP_PASSWORD_HASH` environment
variable. The hash is checked on the server and is never sent to the browser.

Install the dependencies and generate a hash locally:

```powershell
pip install -r requirements.txt
python generate_password_hash.py
```

Copy the complete output hash, including the `$2b$` prefix.

### Posit Cloud project

If the app is launched directly from a Posit Cloud code project, create
`/cloud/project/.Renviron` and add the hash:

```text
APP_PASSWORD_HASH='$2b$12$...complete generated hash...'
```

The `.Renviron` file is ignored by Git and must not be committed. Restart the
project session after creating or changing it, then launch the app again.

### Posit Connect Cloud

If the published app's URL ends in `share.connect.posit.cloud`, open the
content's **Settings**, select **Variables**, and add a secret variable named
`APP_PASSWORD_HASH` with the complete generated hash as its value. Republish or
restart the content.

Authentication lasts for the current Shiny session. Closing the session requires
the password again.
