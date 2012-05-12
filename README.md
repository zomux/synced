Synced
===========

This project's goal is just to make it simple for guys who crazy in serval services,

and have a dream to make them looks united.

## So, How simple it is?

you just need to write a config file (config.yaml) in the root path

it looks like this:
   
    - mode: forward_by_title
      source: 
        service: evernote
        shared_url: "https://www.evernote.com/pub/user/notebook" 

      target:
        service: wordpress
        xmlrpc_url: "http://yourwordpressblog.com/xmlrpc.php"
        username: "yourname"
        password: "xxxxxxxx"
        title: "{title}"
        content: "{content}"
        categories: "dairy"

after your configuration has been done, just run

$ python synced.py

then your dream comes true

## Hey, what service can I use?

okey, now it supports evernote(fetch) , wordpress(fetch,post)

Dont worry , after you had a glance with some codes in it.

it will not cost 30 minutes for you to intergate a new service into it.

If you writed a new service for it , you can upload it to somewhere and give me a link -> zomux [at] hotmail [dot] com.