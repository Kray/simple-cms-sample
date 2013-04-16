<!doctype html>
<html>
<head>
  <title>{{title or 'No title'}} - {{layout.title}}</title>
  <meta charset="utf-8"/>
  <link rel="stylesheet" type="text/css" href="/static/style.css">
  <script src="/static/jquery.min.js"></script>
  <script src="/static/page-edit.js"></script>
</head>
<body>
  <p id="admin-link">
    <a href="/_/">admin</a>
  </p>
  <header>
    <h1>{{layout.title}}</h1>
  </header>
  <div id="navbar">
    {{!layout.navbar}}
  </div>
  <div id="content">
    %include
  </div>
</body>
</html>