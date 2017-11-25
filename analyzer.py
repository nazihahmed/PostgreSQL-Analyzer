#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2

DBNAME = 'news'


def top3articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = \
        """
      SELECT a.title,b.views FROM
      (
      SELECT slug, title FROM articles
      ) a
      JOIN
      (
      SELECT substring(path FROM 10) AS path2,count(id) AS views FROM log
      WHERE path != '/'
      GROUP BY path
      ) b
      ON a.slug = b.path2
      GROUP BY b.views,a.title
      ORDER BY b.views desc
      LIMIT 3
  """
    c.execute(query)
    return c.fetchall()
    db.close()


def bestauthors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = \
        """
    SELECT b.name,a.total FROM
    (
        SELECT author,SUM(views) AS total FROM
        (
            SELECT a.author,b.views FROM
           (
           SELECT slug, author FROM articles
           ) a
           JOIN
           (
           SELECT substring(path FROM 10) AS path2,count(id) AS views FROM log
           WHERE path != '/'
           GROUP BY path
           ) b
            ON a.slug = b.path2
            GROUP BY a.author,b.views
            ORDER BY a.author
        ) AS c
        GROUP BY author
    ) a
    JOIN
    (
        SELECT name,id  FROM authors
    ) b
    ON a.author = b.id
    ORDER BY a.total DESC;
  """
    c.execute(query)
    return c.fetchall()
    db.close()


def mosterrors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = \
        """
    SELECT a.status, a.percentage,a.date1 FROM
    (
        SELECT *,
        round(a.num::numeric/(b.num2+a.num)::numeric*100,2)
        AS percentage FROM
           (SELECT log.status,log.time::date AS date1,count(log.path)
           AS num FROM log
           WHERE status NOT LIKE '%200%'
           GROUP BY status,time::date
           ORDER BY num desc) a
        INNER JOIN
           (SELECT log.status AS status2,log.time::date AS date2,
           count(log.path)
           AS num2 FROM log
           WHERE log.status LIKE '%200%'
           GROUP BY status,log.time::date
           ORDER BY num2 desc) b
        ON a.date1 = b.date2 and a.num::numeric/(b.num2+a.num)::numeric*100 > 1
        ORDER BY percentage desc
    ) AS a
    """
    c.execute(query)
    return c.fetchall()
    db.close()


top3art = top3articles()
print 'Most popular three articles of all time:'
for (article, views) in top3art:
    print "article '{}' has {} views".format(
        article,
        views)
print '-------------------------------'

bestauth = bestauthors()
print 'most popular article authors of all time:'
for (author, views) in bestauth:
    print "author '{}' has {} views".format(author, views)
print '-------------------------------'

mosterr = mosterrors()
print 'the days when more than 1% of requests lead to errors:'
for (status, percentage, date) in mosterr:
    print """error status '{}'
    occured {}% in {}""".format(status, percentage, date)
print '-------------------------------'
