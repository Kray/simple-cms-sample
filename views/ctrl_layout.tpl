%include ctrl_header current='layout'

<h3>Navbar</h3>
<table>
  <thead>
    <tr>
      <td>URL</td>
      <td>Content</td>
      <td><a href="/_/layout/new/navbar">New</a></td>
    </tr>
  </thead>
  <tbody>
%for entry in navbar:
  <form action="/_/layout/edit/{{entry[0]}}" method="post">
    <tr>
      <td><input type="text" name="key" value="{{entry[1] or ''}}"/></td>
      <td><input type="text" name="value" value="{{entry[2] or ''}}"/></td>
      <td><input type="submit" value="Save" name="save"/></td>
    </tr>
  </form>
%end
  </tbody>
</table>
</form>

%rebase layout layout=layout, title='Control'