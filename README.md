# Meeshkan on Udemy

Welcomd to the GitHub project for our AWESOME Udemy course where we use Machine Learning to tell the difference between [Teenage Mutant Ninja Turtles](https://en.wikipedia.org/wiki/Teenage_Mutant_Ninja_Turtles) and [Koopa Troopas](https://en.wikipedia.org/wiki/Koopa_Troopa).

## How to use

### Meeshkan sign up

First, make sure that you have your Meeshkan API Key saved in a file called `.meeshkan/credentials` located in your **home** directory.  To get your Meeshkan API key, sign up on [meeshkan.com](https://www.meeshkan.com) and check out the docs at [meeshkan.com/docs](https://www.meeshkan.com/docs).

### Slack workspace

To sign up for the course's Slack workspace, [click here](https://join.slack.com/t/meeshkan-community/shared_invite/enQtNTA5NjIyMzU0MjkyLTE3YjhlNGRlNjM4OTk0OGE1ODE4YWM3NzZkMTkwODVjNWUzMjA3YjFmMWI1NmNjZmJmM2VkN2I3YmE5Nzk0NTU).

Then, from your [Meeshkan dashboard](https://www.meeshkan.com/app), click **Install on Slack** and make sure to use the meeshkan-community workspace on the top-left corner and the **Slackbot** channel in the **Post to** picker.

![GitHub Logo](/meeshkan_registration.jpg)

### Create Python environment
Meeshkan client requires **Python version >= 3.6.2** so check that you're using recent enough Python! Then create a [virtual environment](https://virtualenv.pypa.io/en/latest/) with
```
$ virtualenv .venv
$ source .venv/bin/activate
```
Make sure your virtual environment is **always** activated for the following commands.

Then, you can install the dependencies for the project with the following command.

```
$ pip install -r requirements.txt
```

### Get some TMNT and Koopa Troopa images

First, let's get some Teenage Mutant Ninja Turtle images!

```
$ mkdir -p dataset/tmnt && python search_bing_api.py --query "teenage mutant ninja turtles" --query "teenage mutant ninja turtles cartoon" --query "teenage mutant ninja turtles leonardo" --query "teenage mutant ninja turtles michelangelo" --query "teenage mutant ninja turtles raphael" --output dataset/tmnt
```
Note that this could take half an hour to one hour depending on your network speed.

Then, to get the Koopa Troopa images.

```
$ mkdir -p dataset/koopa && python search_bing_api.py --query "koopa troopa" --query "koopa paratroopa" --query "koopa red" --query "koopa troopa costume" --output dataset/koopa
```

### Partition and convert the dataset
Partition images in `dataset` into `train` and `test` folders:
```
$ python partition_into_test_and_train.py
```
Note that images are deleted from `dataset` folder!

Then, run the following command to get rid of any RGBA images. To do this, first install [ImageMagick](https://www.imagemagick.org).
```
$ python convert_all_pngs_to_jpgs.py
```

### Run the training
To receive notifications to Slack every 5 minutes, use the following commands.
```
$ meeshkan start
$ meeshkan submit --name transfer_learning --report-interval 300 python transfer_learning.py 
```

Note that, by default, the script activates model checkpointing, which results in a model being saved every epoch.  As the model is ~150 MB, you will most likely want to delete the checkpointed models from time to time or disable them by removing the model `ModelCheckpoint` callback.

### Working with `meeshkan`

List submitted jobs:
```bash
$ meeshkan list
```

Print logs for job named `transfer_learning`:
```bash
$ meeshkan logs transfer_learning
```

Print the latest reported scalar values for the job:
```bash
$ meeshkan report transfer_learning
```

Print notification history for the job:
```bash
$ meeshkan notifications transfer_learning
```

### Make some predictions!

The real fun of this project is that we can predict whether "real" turtles look more like TMNTs or Koopa Troopas.

To grab some pictures of real turtles, run the following command.
```
$ mkdir -p predict/turtle && python search_bing_api.py --query "turtle" --query "turtle face" --query "cute turtle" --query "turtle close up" --output predict/turtle
```

Then, run

```
$ python make_predictions -m your_model_file_name.h5 -p predict/turtle
