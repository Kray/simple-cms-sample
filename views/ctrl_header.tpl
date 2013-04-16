%tabs = [ ('pages', 'Pages'), ('layout', 'Layout'), ('config', 'Configuration') ]

<div class="subnav">
%for key, name in tabs:
  <span>
  %if key != current:
    <a href="{{key}}">
  %end
  {{name}}
  %if key != current:
    </a>
  %end
  </span>
%end
</div>