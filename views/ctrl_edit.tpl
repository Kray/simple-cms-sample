%if defined('url'):
    <form action="/_/edit/{{url}}" method="post">
%else:
    <form action="/_/new" method="post">
%end
  <div>
    <label>Page title</label>
    <input type="text" name="page_title"
%if defined('title'):
    value="{{title}}"
%end
    />
  </div>
  <div>
    <label>Page url</label>
%if defined('url'):
    <span>/{{url}}</span>
%else:
    <span>/</span><input type="text" name="page_url"/>
%end
  </div>
  <div class="page-edit">
    <noscript>
      <p class="warning">Dynamic editing unavailable because your browser has Javascript disabled</p>
    </noscript>
    <div class="page-edit-controls" style="display:none;">
      <span onClick="javascript:pageEditBold(this);"><strong>B</strong></span>
      <span onClick="javascript:pageEditItalic(this);"><i>I</i></span>
      <span onClick="javascript:pageEditUrl(this);" style="text-decoration:underline">URL</span>
    </div>
    <textarea class="page-edit-textarea" name="page_content" style="width:100%; min-height: 10em;">
%if defined('content'):
{{content}}
%end
</textarea>
  </div>
  <div>
    <input type="submit" value="Save"/>
  </div>
</form>
%rebase layout layout=layout, title='Edit page'