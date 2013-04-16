
%if last_failed:
  <p class="warning">User name or password invalid</p>
%end

<form action="/_/login" method="post">
  <div>
    <label>User</label>
    <input type="text" name="user"/>
  </div>
  <div>
    <label>Password</label>
    <input type="password" name="password"/>
  </div>
  <input type="submit" value="Log in"/>
</form>
%rebase layout layout=layout, title='Log in'