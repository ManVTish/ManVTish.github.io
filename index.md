---
layout: default
title: Manish Roy
---
<section class="intro">
  <h1>I build backend systems and write down what I learn.</h1>
  <p>Full-stack engineer based in Pune, mostly Ruby on Rails, currently going deep on LLMs, RAG and agents. This site has the projects I'm proudest of and a log of what I'm learning.</p>
</section>

<section>
  <h2>Selected projects</h2>
  {% include projects.html featured_only=true %}
  <p><a href="{{ '/projects/' | relative_url }}">All projects</a></p>
</section>

<section>
  <h2>Latest from the learning log</h2>
  <ul class="posts">
  {% for post in site.posts limit:3 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a><span class="date">{{ post.date | date: "%-d %b %Y" }}</span></li>
  {% endfor %}
  </ul>
  <p><a href="{{ '/blog/' | relative_url }}">Everything I've written</a></p>
</section>
