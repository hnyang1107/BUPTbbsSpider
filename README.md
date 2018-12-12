# [北京邮电大学校园bbs（镜像）](http://bbs.cloud.icybee.cn/)爬虫

## 运行方法

在`./BUPTbbsSpider`目录下运行

```bash
scrapy crawl bupt_s1
```

或者在`bash`下后台运行运行（需修改`run.py`内的爬虫名）

````bash
nohup python -u run.py > run.log 2>&1 &
````

可实现后台抓取[`S1`](http://bbs.cloud.icybee.cn/section/1)版块，并保存在`BUPTData`文件夹下，存储为`csv`文件.

## 抓取内容

|     字段      |    中文名称     |                             示例                             |
| :-----------: | :-------------: | :----------------------------------------------------------: |
| board_name_cn |   板块中文名    |                           北邮关注                           |
| board_name_en |   板块英文名    |                            Focus                             |
|    content    |  发帖[^*]内容   | 今年应届渣硕，在今年秋招中各种花式跪，目前为止找到一个银行分行的金融科技的岗位，在深圳。如果接下来没有更好的选择可能只能去银行了 |
|    post_id    |    发帖人id     |                           ihuazuo                            |
|   post_sex    |   发帖人性别    |                             男生                             |
|   post_time   |    发帖时间     |                   Sun Nov 18 18:36:08 2018                   |
|  post_title   |    帖子标题     |           【问题】去银行以后的职业发展是怎么样的呢           |
|   reply_id    |    回复对象     |                     *（若无则为空字符）*                     |
| thread_owner  | 主题发起者[^**] |                           ihuazuo                            |
| thread_title  |    主题标题     |  [由neuq51221推荐]【问题】去银行以后的职业发展是怎么样的呢   |
|  thread_url   |    主题链接     |        http://bbs.cloud.icybee.cn/article/Kungfu/105         |

[*]: 创建新的主题或者回复新主题统称为发帖
[**]: 这里指帖子组（主题）发起者，即楼主

