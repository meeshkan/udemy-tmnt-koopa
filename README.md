# Meeshkan on Udemy

Welcomd to the GitHub project for our AWESOME Udemy course where we use Machine Learning to tell the difference between [Teenage Mutant Ninja Turtles](https://en.wikipedia.org/wiki/Teenage_Mutant_Ninja_Turtles) and [Koopa Troopas](https://en.wikipedia.org/wiki/Koopa_Troopa).

## How to use

### Meeshkan sign up

First, make sure that you have your Meeshkan API Key saved in a file called `.meeshkan/credentials` located in your **home** directory.  To get your Meeshkan API key, sign up on [meeshkan.com](https://www.meeshkan.com) and check out the docs at [meeshkan.com/docs](https://www.meeshkan.com/docs).

### Slack workspace

To sign up for the course's Slack workspace, [click here](https://join.slack.com/t/meeshkan-community/shared_invite/enQtNTA5NjIyMzU0MjkyLTE3YjhlNGRlNjM4OTk0OGE1ODE4YWM3NzZkMTkwODVjNWUzMjA3YjFmMWI1NmNjZmJmM2VkN2I3YmE5Nzk0NTU).

Then, from your Meeshkan dashboard, click **Install on Slack** and make sure to use the meeshkan-community workspace on the top-left corner and the **Slackbot** channel in the **Post to** picker.

![GitHub Logo](/meeshkan_registration.jpg)

### Create Python environment
Meeshkan client requires **Python version >= 3.6.2** so check that you're using recent enough Python! Then create a [virtual environment](https://virtualenv.pypa.io/en/latest/) with
```
$ virtualenv .venv
$ source .venv/bin/activate
```
Make sure your virtual environment is **always** activated for the following commands.

### Install the dependencies
```
$ pip install -r requirements.txt
```

### Get some TMNT images

```
$ mkdir -p dataset/tmnt && python search_bing_api.py --query "teenage mutant ninja turtles" --query "teenage mutant ninja turtles cartoon" --query "teenage mutant ninja turtles leonardo" --query "teenage mutant ninja turtles michelangelo" --query "teenage mutant ninja turtles raphael" --output dataset/tmnt
```
Note that this could take half an hour to one hour depending on your network speed.

### Get some Koopa Troopa images

```
$ mkdir -p dataset/koopa && python search_bing_api.py --query "koopa troopa" --query "koopa paratroopa" --query "koopa red" --query "koopa troopa costume" --output dataset/koopa
```

### Partition the dataset
```
$ python partition_into_test_and_train.py
```

### Convert pngs to jpgs
This gets rid of any RGBA images. To do this, first install [ImageMagick](https://www.imagemagick.org).
```
$ python convert_all_pngs_to_jpgs.py
```

### Run the training
To receive notifications to Slack every 5 minutes, use the following commands.
```
$ meeshkan start
$ meeshkan submit --name transfer_learning --report-interval 300 python transfer_learning.py 
```
