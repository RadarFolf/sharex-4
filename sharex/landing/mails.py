WELCOME_EMAIL = """\
Hi, this is Martin from sharex.

Thanks for joining our society. This is exciting!

Like you, many interesting, up-and-coming startups has signed up and are ready to connect with other valuable startups. We are now working on connecting you with awesome startups.

If you have any feedback or are curious about the process, we would love to skype with you.

Cheers,
Martin from sharex.io
skype: sharexio
+47 45 19 19 91"""

INVITE_EMAIL = """\
Hey! You just got invited to join sharex.io by %s.
Sign up by clicking on the following link,
https://sharex.io/p/signup/%s?email=%s

Cheers,
Team sharex
skype: sharexio"""

def get_invite_email(sender, to, startup):
	return INVITE_EMAIL % (sender, startup, to)

