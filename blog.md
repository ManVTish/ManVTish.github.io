---
layout: default
title: Learning log
permalink: /blog/
---
<h1>Learning log</h1>
<p class="lede">Short notes on things I'm learning, written to understand them properly.</p>
<ul class="posts">
{% for post in site.posts %}
  <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a><span class="date">{{ post.date | date: "%-d %b %Y" }}</span>
  {% if post.tags.size > 0 %}<span class="tags">{{ post.tags | join: ", " }}</span>{% endif %}</li>
{% endfor %}
</ul>
