%include ctrl_header current='pages'

<table style="pages-table">
  <thead>
    <tr>
      <th>Url</th>
      <th>Title</th>
      <th><a href="/_/new">New page</a></th>
    </tr>
  </thead>
  <tbody>
%for page in pages:
    <tr>
      <td><a href="/{{page['url']}}">/{{page['url']}}</a></td>
      <td><a href="/{{page['url']}}">{{page['title']}}</a></td>
      <td><a href="/_/edit/{{page['url']}}">edit</a></td>
    </tr>
%end
  </tbody>
</table>

%rebase layout layout=layout, title='Control'