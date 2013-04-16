%include ctrl_header current='config'

<h3>All configuration values</h3>
<table>
  <thead>
    <tr>
      <td>Key</td>
      <td>Value</td>
      <td></td>
    </tr>
  </thead>
  <tbody>
%for entry in config:
  <form action="/_/config/" method="post">
    <input type="hidden" name="key" value="{{entry[0] or ''}}"/>
    <tr>
      <td>{{entry[0] or ''}}</td>
      <td><input type="text" name="value" value="{{entry[1] or ''}}"/></td>
      <td><input type="submit" value="Save" name="save"/></td>
    </tr>
  </form>
%end
  <form action="/_/config/" method="post">
    <tr>
      <td><input type="text" name="key" value=""/></td>
      <td><input type="text" name="value" value=""/></td>
      <td><input type="submit" value="Create" name="create"/></td>
    </tr>
  </form>
  </tbody>
</table>
</form>

%rebase layout layout=layout, title='Control'