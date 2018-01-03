job = function(job) {
    document.addEventListener('DOMContentLoaded', function() {
        var offset = 0;
        var ansi_up = new AnsiUp;
        var code = document.getElementById('log');

        var fn = function() {
            fetch('/logs/' + job.id + '?offset=' + offset, {credentials: 'same-origin'}).then(function(response) {
                return response.text();
            }).then(function(text) {
                var str = text;
                offset += text.length;
                str = str.replace(/^::piper:(command|after_failure):(\d+):start:(\d+)::$/gm, function(m, type, order, time) {
                    if(type === 'command') {
                        type = 'commands';
                    }
                    return '$ ' + job[type][order]['cmd'];
                });

                str = str.replace(/^::piper:(command|after_failure):(\d+):end:(\d+):(\d+)::$/gm, function(m, type, order, time, exitCode) {
                    if(type === 'command') {
                        type = 'commands';
                    }
                    return ''
                });
                code.innerHTML += ansi_up.ansi_to_html(str);
                setTimeout(fn, 1000);
            });
        };

        fn();
    });
};
