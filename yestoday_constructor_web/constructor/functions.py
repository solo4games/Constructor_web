import random
import re
from typing import List
import uuid
import requests
from getcourse.models import Audio
from yestoday_constructor_web.settings import ALLOWED_HOSTS


def srez_v2(str, start, end):
    startID = str.find(start)
    s = str[:startID+len(start)]
    str = str[startID+len(start):]
    endID = str.find(end)
    s += str[endID:]
    return s


def pr_audio(s, galery_number, global_i, global_i_i):
    result_all = """"""
    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
    s = s.split('\n')
    textup = s[0].strip()
    textdown = s[1].strip()
    url = s[2].strip()
    seekbar = bool(int(s[3]))
    audio, created = Audio.objects.get_or_create(
        text_up=textup,
        text_down=textdown,
        seekbar=seekbar,
        src=url,
        file=None,
    )
    if seekbar:
        seekbar = """
        <div>
                    <progress class="podcast-progress" id='podcast-progress' value="0" max="1"
                        onclick="audioTimeLineClick(this, event)"></progress>
                    <div class="f-container" id='f-container'>
                        <div class="podcast-time" id='podcast-time'>00:00 / 00:00</div>
                        <div class="podcast-speed" id='podcast-speed'>
                            <a class="podcast-speed-10 active" href="javascript:void(0)"
                                onclick="audioChangeSpeedClick(this)">1x</a> / <a class="podcast-speed-15"
                                href="javascript:void(0)" onclick="audioChangeSpeedClick(this)">1.5x</a> / <a
                                class="podcast-speed-20" href="javascript:void(0)"
                                onclick="audioChangeSpeedClick(this)">2x</a>
                        </div>
                    </div>
                </div>
        """
    else:
        seekbar = ""

    result = f"""
    <div class='audio-add{audio.id} audio-div' id='audio-add'>
            <audio class="audio-player{audio.id}" id='audio-player' src="{'https://'+ALLOWED_HOSTS[0]+audio.file.url.replace('media/', 'get-') if 'api.voicerss.org' in audio.src else audio.src}"
                onended="audioOnEnded(this)" oncanplay="audioOnCanPlay(this)" onplay="audioPlay(this)"
                onpause="audioPause(this)"></audio>
            <div class="podcast-container" id='podcast-container'>
                <div class="h-container" id='h-container'>
                    <div class="podcast-playpause" id='podcast-playpause'>
                        <img class="play" id="play"
                            src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/337/h/cb28b80bb66ad56d3c12fd1885bc3ef8.svg"
                            onclick="playPauseClick(this)">
                        <img class="pause" id="pause"
                            src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/197/h/7395c5433ab34099a1d5b9b139efdd5b.svg"
                            onclick="playPauseClick(this)">
                    </div>
                    <div>
                        <div class="podcast-title" id='podcast-title'>{audio.text_up}
                        <button type="button" onclick="audioSaveBtnClick(this)" id="{audio.id}"><i
                                    class="bi bi-bookmark-star"></i></button></div>
                        <div class="podcast-subtitle" id='podcast-subtitle'>{audio.text_down}</div>
                    </div>
                </div>

            </div>
            {seekbar}

        </div>
        """

    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiz1(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    s = s.split('\n')

    def srez(str, start, end):
        startID = str.find(start)
        str = str[startID+len(start):]
        endID = str.find(end)
        str = str[:endID]
        return str

    news = """"""
    mass = []
    d = {}
    j = 0
    for el in s:
        news += """            <p>"""
        stars = []
        elcopy = el
        for n in range(len(el)):
            if el[n] == '*':
                stars.append(n)
        elcopy = el
        st = -2
        end = -1
        for n in range(len(el)):
            if n in stars:
                st = stars.pop(0)
                end = stars.pop(0)
                key = elcopy[st+1:end]
                mass.append(key)
                j += 1
                strj = str(j)
                d[key] = f"key_{i}_{strj}"
                news += f"""<span id = "target" class="target{i}" data-accept{i}="key_{i}_{strj}">&nbsp;</span>"""
            if not (n >= st and n <= end):
                news += el[n]

        news += """</p>
    """
    result = f"""
    <div class="quiz-wrapper{i}" id="quiz-wrapper-quiz1">
        <p class="question-description{i}" id="question-description">Fill in the blanks by dragging the missing answer.</p>
        <ul class="options{i}" id='options'>
            <p class="title{i}" id='title'>Options</p>
    """

    keys = """"""
    j = 0
    random.shuffle(mass)
    for el in mass:
        keys += f"""        <p class="option{i}" id='option' data-target{i}="{d[el]}">{el}</p>\n"""
    result += keys
    result += f"""
        </ul>
        <div class="answers{i}" id='answers'>
            <ol>
    """
    result += news
    result += f"""
            </ol>
        </div>
        <button id='submitquiz1' type="submit{i}" value="submit">Submit</button>

    </div>
    """+"""
    <script src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/208/h/99170efb96f914b9d28bac2931ae570f.js"></script>
    <script>
    """+f"""
            //initialize the quiz options
            var answersLeft{i} = [];
            $('.quiz-wrapper{i}').find('p.option{i}').each( function(i) """+"""{"""+f"""
                var $this{i} = $(this);
                var answerValue{i} = $this{i}.data('target{i}');
                var $target{i} = $('.answers{i} .target{i}[data-accept{i}="'+answerValue{i}+'"]');
                var labelText{i} = $this{i}.html();
                $this{i}.draggable( """+"""{"""+f"""
                    revert: "invalid",
                    containment: ".quiz-wrapper{i}",
                    stop: function(event, ui) """+"""{
                        """+f"""$this{i}.css('color' ,'red');"""+"""
                    }
                });
                """+f"""if ( $target{i}.length > 0 ) """+"""{"""+f"""
                    $target{i}.droppable( """+"""{

                    """+f"""accept: 'p.option{i}[data-target{i}="'+answerValue{i}+'"]',

                    drop: function( event, ui ) """+"""{"""+f"""
                        $this{i}.draggable('destroy');
                        $target{i}.droppable('destroy');
                        $this{i}.html('&nbsp;');
                        $target{i}.html(labelText{i});
                        answersLeft{i}.splice( answersLeft{i}.indexOf( answerValue{i} ), 1 );
                        $target{i}.css('background' ,'lightgreen');"""+"""
                    }
                });
                """+f"""answersLeft{i}.push(answerValue{i});"""+"""
                } else { }
            });
    """
    result += """
            """+f"""$('.quiz-wrapper{i} button[type="submit{i}"]').click( function() """+"""{
        """+f"""if ( answersLeft{i}.length > 0 ) """+"""{"""+"""

                } else {
                    """+f"""
                    ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                    ans{i} = ans{i}-1;
                    $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                    if (ans{i} <= 0)"""+"""{"""+f"""
                        $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                    $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                    }
                    """+"""
                }
            });
        });

    </script>

    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiz2(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    s = s.split('\n')
    ss = s[1]
    s = s[0]
    text_prev = ''
    text_next = ''
    key = ''
    check = 0
    for letter in s:
        if letter != '*' and check == 0:
            text_prev += letter
        elif letter == '*' and check == 0:
            check = 1
        elif letter != '*' and check == 1:
            key += letter
        elif letter == '*' and check == 1:
            check = 2
        elif letter != '*' and check == 2:
            text_next += letter
    ss = ss.split()
    ss.append(key)
    random.shuffle(ss)
    result = """"""
    result += f"""
    <div class="quiz-wrapper{i}" id='quiz-wrapper-quiz2'>
        <div class="answers{i}" id='answers'>
            <div class ="general{i}" id='general'>
                <div class = 'contenttarget{i}' id='contenttarget'>
                    <span class="text{i}" id='text'>{text_prev}</span>
                </div>
                <div class = 'contenttargett{i}' id='contenttargett'>

                    <span class="target{i}" id='target' data-accept{i}="key_{i}_100">&nbsp;</span>
                </div>
                <div class = 'contenttarget{i}' id='contenttarget'>
                    <span class="text{i}" id='text'>{text_next}</span>
                </div>
            </div>
        </div>
        <ul class="options{i}" id='options'>
    """
    j = 1
    r = """"""
    for el in ss:
        if el == key:
            r += f"""
                <li class="option{i}" id='option' data-target{i}="key_{i}_100">{el}</li>
            """
        else:
            r += f"""
                <li class="option{i}" id='option' data-target{i}="key_{i}_{j}">{el}</li>
            """
        j += 1
    result += r
    result += f"""
        </ul>
        <button id='submitquiz2' type="submit{i}" value="submit">Submit</button>

    </div>
    """+"""
    <script src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/208/h/99170efb96f914b9d28bac2931ae570f.js"></script>

    <script>

    """+f"""
            //initialize the quiz options
            var answersLeft{i} = [];
            $('.quiz-wrapper{i}').find('li.option{i}').each( function(i) """+"""{"""+f"""
                var $this{i} = $(this);
                var answerValue{i} = $this{i}.data('target{i}');
                var $target{i} = $('.answers{i} .target{i}[data-accept{i}="'+answerValue{i}+'"]');
                var labelText{i} = $this{i}.html();
                $this{i}.draggable( """+"""{"""+"""
                    revert: "invalid",

                    stop: function(event, ui) """+"""{
                        """+f"""
                        //$this{i}.css('color' ,'white');
                        $this{i}.css('border' ,'1px solid #F05C5C'); """+"""

                    }
                });
                """+f"""if ( $target{i}.length > 0 ) """+"""{"""+f"""
                    $target{i}.droppable( """+"""{

                    """+f"""accept: 'li.option{i}[data-target{i}="'+answerValue{i}+'"]',

                    drop: function( event, ui ) """+"""{"""+f"""
                        $this{i}.draggable('destroy');
                        $target{i}.droppable('destroy');
                        $this{i}.html('&nbsp;');
                        $target{i}.html(labelText{i});
                        answersLeft{i}.splice( answersLeft{i}.indexOf( answerValue{i} ), 1 );
                        $target{i}.css('border' ,'1px solid #5199FF');
                        $target{i}.css('background' ,'#E0ECFD');
                        $this{i}.css('background' ,'none');
                        $this{i}.css('display', 'none');
                        if ( answersLeft{i}.length == 0 )"""+"""{"""+f"""
                            $('.options{i}').css('display','none');"""+"""
                            """+f"""
                            ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                            ans{i} = ans{i}-1;
                            $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                            if (ans{i} <= 0)"""+"""{"""+f"""
                                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                            }
                            """+"""
                        }
                    }
                });
                """+f"""answersLeft{i}.push(answerValue{i});"""+"""
                } else { }
            });
    </script>
    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiz3(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    s = s.split()

    result = f"""<div class="quiz-wrapper{i}" id='quiz-wrapper-quiz3'>
        <div class="answers{i}" id='answers'>
            <div class ="general{i}" id='general'>
    """
    r = """"""
    rr = """"""
    keys = {}
    left = 0
    dlina = len(s)

    for n in range(len(s)):
        if dlina > 2 or len(s) <= 4:

            r += f"""
                <div class = 'contenttarget{i}' id='contenttarget'>
                    <span class="target{i}" id='target' data-accept{i}="key_{i}_{n}">&nbsp;</span>
                </div>
                """
            keys[s[n]] = f"key_{i}_{n}"
            dlina -= 1
        else:
            left += 1
            rr += f"""
                <div class = 'contenttarget{i}' id='contenttarget'>
                    <span class="target{i}" id='target' data-accept{i}="key_{i}_{n}">&nbsp;</span>
                </div>
                """
            keys[s[n]] = f"key_{i}_{n}"
            dlina -= 1

    dlina = len(s)
    if left == 1 or left == 2:
        r += """
                <div>
                </div>
        """
    r += rr

    r += """
            </div>
    """
    result += r

    result += f"""
        </div>

        <ul class="options{i}" id='options'>
        """
    r = """"""
    rr = """"""
    random.shuffle(s)
    last = left
    for n in range(len(s)-last):
        r += f"""
            <div class = 'contentoptions{i}' id='contentoptions'>
                <li class="option{i}" id='option' data-target{i}="{keys[s[n]]}">{s[n]}</li>
            </div>
        """
    result += r
    # result+="""
    #    </ul>
    # """
    if last != 0:
        for n in range(last):
            rr += f"""
            <div class = 'contentoptions{i}' id='contentoptions'>
                <li class="option{i}" id='option' data-target{i}="{keys[s[(-1*(n+1))]]}">{s[(-1*(n+1))]}</li>
            </div>
            """
    if left == 1 or left == 2:
        result += """
            <div></div>
        """
    result += rr

    result += f"""
        </ul>
        <button type="submit{i}" id='submitquiz3' value="submit">Submit</button>
    </div>
    """+"""
    <script src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/208/h/99170efb96f914b9d28bac2931ae570f.js"></script>
    """+"""
    <script>
    """+f"""
            //initialize the quiz options
            var answersLeft{i} = [];
            $('.quiz-wrapper{i}').find('li.option{i}').each( function(i) """+"""{"""+f"""
                var $this{i} = $(this);
                var answerValue{i} = $this{i}.data('target{i}');
                var $target{i} = $('.answers{i} .target{i}[data-accept{i}="'+answerValue{i}+'"]');
                var labelText{i} = $this{i}.html();
                $this{i}.draggable( """+"""{"""+"""
                    revert: "invalid",

                    stop: function(event, ui) """+"""{
                        """+f"""//$this{i}.css('color' ,'white');
                            $this{i}.css('border' ,'1px solid #F05C5C'); """+"""

                    }
                });
                """+f"""if ( $target{i}.length > 0 ) """+"""{"""+f"""
                    $target{i}.droppable( """+"""{

                    """+f"""accept: 'li.option{i}[data-target{i}="'+answerValue{i}+'"]',

                    drop: function( event, ui ) """+"""{"""+f"""
                        $this{i}.draggable('destroy');
                        $target{i}.droppable('destroy');
                        $this{i}.html('&nbsp;');
                        $target{i}.html(labelText{i});
                        answersLeft{i}.splice( answersLeft{i}.indexOf( answerValue{i} ), 1 );
                        $target{i}.css('border' ,'1px solid #5199FF');
                        $target{i}.css('background' ,'#E0ECFD');
                        $this{i}.css('background' ,'none');
                        $this{i}.css('display', 'none');
                        if ( answersLeft{i}.length == 0 )"""+"""{"""+f"""
                            $('.options{i}').css('display','none');"""+"""
                            """+f"""
                            ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                            ans{i} = ans{i}-1;
                            $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                            if (ans{i} <= 0)"""+"""{"""+f"""
                                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                            }
                            """+"""
                        }
                    }
                });
                """+f"""answersLeft{i}.push(answerValue{i});"""+"""
                } else { }
            });

    </script>
    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiz4(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    file = s.split('\n')
    check = 0
    parsed = """"""
    keys = []
    keysd = {}
    j = 0
    for line in file:
        parsed += """
            <span class="text10" id='text'>
    """
        for word in line:
            if word == '*' and check == 0:
                j += 1
                keyfor = f"key_{i}_{j}"
                parsed += f"""<span class="target{i}" id='target' data-accept{i}="{keyfor}">&nbsp;</span>"""
                check = 1
                key = ''
            elif word == '*' and check == 1:
                check = 0
                keys.append(key)
                keysd[key] = keyfor
            elif word != '*' and check == 1:
                key += word
            else:
                parsed += word

        parsed += """</span>
            <br>"""

    result = """"""
    result += f"""
    <div class="quiz-wrapper{i}" id='quiz-wrapper-quiz4'>
        <ul class="options{i}" id='options'>
    """
    random.shuffle(keys)
    for el in keys:
        result += f"""
            <li class="option{i}" id='option' data-target{i}="{keysd[el]}">{el}</li>
    """

    result += f"""
        </ul>
        <div class="answers{i}" id='answers'>
    """
    result += parsed
    result += f"""
        </div>

        <button type="submit{i}" id='submitquiz4' value="submit">Submit</button>
    </div>
    """+"""
    <script src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/208/h/99170efb96f914b9d28bac2931ae570f.js"></script>
    <script>
    """+f"""
            //initialize the quiz options
            var answersLeft{i} = [];
            $('.quiz-wrapper{i}').find('li.option{i}').each( function(i) """+"""{"""+f"""
                var $this{i} = $(this);
                var answerValue{i} = $this{i}.data('target{i}');
                var $target{i} = $('.answers{i} .target{i}[data-accept{i}="'+answerValue{i}+'"]');
                var labelText{i} = $this{i}.html();
                $this{i}.draggable( """+"""{"""+"""
                    revert: "invalid",

                    stop: function(event, ui) """+"""{
                        """+f"""//$this{i}.css('color' ,'white');
                            $this{i}.css('border' ,'1px solid #F05C5C'); """+"""

                    }
                });
                """+f"""if ( $target{i}.length > 0 ) """+"""{"""+f"""
                    $target{i}.droppable( """+"""{

                    """+f"""accept: 'li.option{i}[data-target{i}="'+answerValue{i}+'"]',

                    drop: function( event, ui ) """+"""{"""+f"""
                        $this{i}.draggable('destroy');
                        $target{i}.droppable('destroy');
                        $this{i}.html('&nbsp;');
                        $target{i}.html(labelText{i});
                        answersLeft{i}.splice( answersLeft{i}.indexOf( answerValue{i} ), 1 );
                        $target{i}.css('border' ,'1px solid #5199FF');
                        $target{i}.css('background' ,'#E0ECFD');
                        $this{i}.css('background' ,'none');
                        $this{i}.css('display', 'none');
                        if ( answersLeft{i}.length == 0 )"""+"""{"""+f"""
                            $('.options{i}').css('display','none');"""+"""
                            """+f"""
                            ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                            ans{i} = ans{i}-1;
                            $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                            if (ans{i} <= 0)"""+"""{"""+f"""
                                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                            }
                            """+"""
                        }
                    }
                });
                """+f"""answersLeft{i}.push(answerValue{i});"""+"""
                } else { }
            });
    </script>

    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiz5(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    ans = s.split('\n')
    ifNeedWords = ans[1]
    ans = ans[0].strip()

    anssh = ans.split()
    random.shuffle(anssh)
    ansshstr = ''
    if '1' in ifNeedWords:
        for w in anssh:
            ansshstr += w+' / '
        ansshstr = ansshstr[:-1]

    s = f"""
        <div id='quiz-wrapper-quiz5' quiz-uuid="{str(uuid.uuid4())}">
            <div class="textbck" id='textbck'>
                <p class="task" id='task' answer='{ans}' tries="0">{ansshstr}</p>
                <div class="text__but" id='text__but'>
                    <div class="textareadiv" id='textareadiv'>
                        <textarea class="textarea" id='textarea'
                            onfocus="if(this.value==this.defaultValue)this.value='';"
                            onblur="if(this.value=='')this.value=this.defaultValue;">Начните писать...
                       
                        </textarea>
                        <div class="mistakestext" id='mistakestext' onclick="showTextAreaQuiz5(this)">
                        </div>
                    </div>
                    <div class="buttoncheck" id='buttoncheck'>
                        <button type="check" id='submitquiz5' value="check"
                            onclick="checkAnswerQuiz5(this)">✔</button>
                        <button class="showans" id="showans" onclick="showAnsQuiz5(this)">Показать
                            ответ</button>
                    </div>
                </div>
                <div class="translateddiv" id='translateddiv'>
                    <p class="translatedtext" id='translatedtext'>Правильный ответ: {ans}</p>
                </div>
            </div>
        </div>
    """

    result_all += s
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_cards(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    file = s.split('\n')

    answers = []
    answerskeys = {}
    k = 1
    for line in file:
        if line != '' and line != ' ':
            newline = line.split(';')
            answers.append(newline[0])
            answerskeys[newline[0]] = [newline[1], newline[2]]
    s = f"""
    <div class="demo{i}" id='demo'>
        <div class='end__check{i}' id='end__check'>
    """
    answersstr = """"""
    k = 1
    for a in answers[::-1]:
        answersstr += f"""
            <p class='end__check__ans{k}_{i}' id='end__check__ans'>{k}. {a} - {answerskeys[a][0]}</p>"""
        k += 1
    answersstr += f"""
            <p class='end__check__anss{i}' id='end__check__anss'></p>
            <button type="repeat{i}" id='repeatcards' value="repeat{i}">Начать заново</button>
    """
    s += answersstr
    colors = ['blue', 'purple', 'brown', 'indigo', 'cyan', 'lime']
    s += f"""
        </div>
        <div class="demo__content{i}" id='demo__content'>
            <div class="demo__card-cont{i}" id='demo__card-cont'>
    """
    cardsstr = """"""
    for card in answers:
        cardsstr += f"""
                <div class="demo__card{i}" id='demo__card'>
                    <div class="demo__card__top{i} {colors[random.randint(0,len(colors)-1)]}" id='demo__card__top'>
                        <div class="demo__card__img{i}" id='demo__card__img'>
                            <img class="demo__card__img__image{i}" src="{answerskeys[card][1]}" id='demo__card__img__image'>
                        </div>
                        <p class="demo__card__name{i}" id='demo__card__name'>{card}</p>
                    </div>
                    <div class="demo__card__btm{i}" id='demo__card__btm'>
                        <p class="demo__card__we{i}" id='demo__card__we'>{answerskeys[card][0]}</p>
                    </div>
                    <div class="demo__card__choice{i} m--reject" id='demo__card__choice__reject'></div>
                    <div class="demo__card__choice{i} m--like" id='demo__card__choice__like'></div>
                    <div class="demo__card__drag{i}" id='demo__card__drag'></div>
                </div>
    """
    s += cardsstr
    s += f"""
            </div>
            <p class="demo__tip{i}" id='demo__tip'>Swipe left or right</p>
        </div>
    </div>
    """+"""
    <script>
        $(document).ready(function() {"""+f"""

            var animating{i} = false;
            var cardsCounter{i} = 0;
            var numOfCards{i} = {len(answers)};
            var curNum{i} = 0;
            var numTrue{i} = 0;
            var decisionVal{i} = 80;
            var pullDeltaX{i} = 0;
            var deg{i} = 0;
            var $card{i}, $cardReject{i}, $cardLike{i};
            var answers{i} = [];
            """+f"""
            function pullChange{i}() """+"""{"""+f"""
                animating{i} = true;
                deg{i} = pullDeltaX{i} / 10;
                $card{i}.css("transform", "translateX("+ pullDeltaX{i} +"px) rotate("+ deg{i} +"deg)");

                var opacity{i} = pullDeltaX{i} / 100;
                var rejectOpacity{i} = (opacity{i} >= 0) ? 0 : Math.abs(opacity{i});
                var likeOpacity{i} = (opacity{i} <= 0) ? 0 : opacity{i};
                $cardReject{i}.css("opacity", rejectOpacity{i});
                $cardLike{i}.css("opacity", likeOpacity{i});"""+"""
            };
            """+f"""
            function release{i}() """+"""{"""+f"""

                if (pullDeltaX{i} >= decisionVal{i}) """+"""{"""+f"""
                    $card{i}.addClass("to-right");
                    curNum{i} = curNum{i} + 1;
                    numTrue{i} = numTrue{i} + 1;
                    answers{i}.push('r');"""+"""
                } else if """+f"""(pullDeltaX{i} <= -decisionVal{i}) """+"""{"""+f"""
                    $card{i}.addClass("to-left");
                    curNum{i} = curNum{i} + 1;
                    answers{i}.push('l');"""+"""
                }
                if (Math.abs"""+f"""(pullDeltaX{i}) >= decisionVal{i}) """+"""{"""+f"""
                    $card{i}.addClass("inactive");

                    setTimeout(function() """+"""{"""+f"""
                        $card{i}.addClass("below").removeClass("inactive to-left to-right");
                        cardsCounter{i}++;
                        if (cardsCounter{i} === numOfCards{i}) """+"""{"""+f"""
                            cardsCounter{i} = 0;
                            $(".demo__card{i}").removeClass("below");"""+"""
                        }
                    }, 300);
                }
                """+f"""
                if (Math.abs(pullDeltaX{i}) < decisionVal{i}) """+"""{"""+f"""
                    $card{i}.addClass("reset");"""+"""
                }

                setTimeout(function() {"""+f"""
                    $card{i}.attr("style", "").removeClass("reset")
                    .find(".demo__card__choice{i}").attr("style", "");

                    pullDeltaX{i} = 0;
                    animating{i} = false;"""+"""
                }, 300);
                """+f"""
                if (curNum{i} == numOfCards{i})"""+"""{"""+f"""
                    $('.demo__content{i}').css('display','none');
                    for (let i = 0; i < numOfCards{i}; i++) """+"""{"""+f"""
                        var cl{i} = '';
                        """+f"""
                        ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                        ans{i} = ans{i}-1;
                        $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                        if (ans{i} <= 0)"""+"""{"""+f"""
                            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                    $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                        }
                        """+f"""
                        if (answers{i}[i] == 'r')"""+"""{"""+f"""
                            cl{i} = '.end__check__ans'+ (i+1).toString() + '_{i}';
                            $(cl{i}).css('color','#31979b');"""+"""
                        }
                        else{"""+f"""
                            cl{i} = '.end__check__ans'+ (i+1).toString() + '_{i}';
                            $(cl{i}).css('color','#F05C5C');"""+"""
                        }
                    }
                    """+f"""
                    var trans{i} = 'Верных ответов '+ numTrue{i}.toString()+'/'+numOfCards{i}.toString();
                    $('.end__check__anss{i}').html(trans{i});
                    $('.end__check{i}').css('display','block');"""+"""
                }
            };
            """+f"""
            $('.demo__card{i}').click( function() """+"""{"""+f"""
                if ($(this).find('.demo__card__we{i}').css('display') == 'none')"""+"""{"""+f"""
                    $(this).find('.demo__card__we{i}').css('display','flex');"""+"""
                }
                else{"""+f"""
                    $(this).find('.demo__card__we{i}').css('display','none');"""+"""
                }
            });
            """+f"""
            $(document).on("mousedown touchstart", ".demo__card{i}:not(.inactive)", function(e)"""+"""{"""+f"""
                if (animating{i}) return;
                $card{i} = $(this);
                $cardReject{i} = $(".demo__card__choice{i}.m--reject", $card{i});
                $cardLike{i} = $(".demo__card__choice{i}.m--like", $card{i});
                var startX{i} =  e.pageX || e.originalEvent.touches[0].pageX;

                $(document).on("mousemove touchmove", function(e) """+"""{"""+f"""
                    var x{i} = e.pageX || e.originalEvent.touches[0].pageX;
                    pullDeltaX{i} = (x{i} - startX{i});
                    if (!pullDeltaX{i}) return;
                    pullChange{i}();"""+"""
                });

                $(document).on("mouseup touchend", function() {"""+f"""
                    $(document).off("mousemove touchmove mouseup touchend");
                    if (!pullDeltaX{i}) return; // prevents from rapid click events
                    release{i}();"""+"""
                });
            });
            """+f"""
            $('.end__check{i} button[type="repeat{i}"]').click( function() """+"""{"""+f"""
                $('.end__check{i}').css('display','none');
                $('.demo__content{i}').css('display','inline');
                $('.demo__content{i}').find('.demo__card__we{i}').each( function(i) """+"""{"""+f"""
                    var $this{i} = $(this);
                    $this{i}.css('display','none');"""+"""
                });
                """+f"""
                animating{i} = false;
                cardsCounter{i} = 0;
                numOfCards{i} = {len(answers)};
                numTrue{i} = 0;
                curNum{i} = 0;
                decisionVal{i} = 80;
                pullDeltaX{i} = 0;
                deg{i} = 0;
                answers{i} = [];"""+"""
            });
        });

    </script>
    """
    result_all += s
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quizphoto(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    file = s.split('\n')
    if '' in file:
        file.remove('')

    urls = {}
    keys = {}
    mass = []
    for line in file:
        mass.append(line)
    j = 1
    while mass != []:
        keys[f'key_{i}_{j}'] = mass.pop(0)
        urls[f'key_{i}_{j}'] = mass.pop(0)
        j += 1

    result = f"""
    <div class="quiz-wrapper{i}" id='quiz-wrapper-quizphoto'>
        <ul class="options{i}" id='options'>
    """
    li_str = """"""
    curkeys = keys.items()
    li = []
    for key, value in curkeys:
        string = f"""
            <div class='optiondiv{i}' id='optiondiv'>
                <li class="option{i}" id='option' data-target{i}="{key}">{value}</li>
            </div>
    """
        li.append(string)
    random.shuffle(li)
    for el in li:
        li_str += el
    result += li_str
    result += f"""
        </ul>
        <div class="answers{i}" id='answers'>
                <div class ="general{i}" id='general'>
    """

    span_str = """"""
    currentkeys = []
    cnt = 0
    for key, value in keys.items():
        cnt += 1
        currentkeys.append(key)
        if cnt == 3:

            span_str += f"""
                    <div class = 'contentimg{i}' id='contentimg'>
                        <img class = 'contentcontentimgin{i}' id='contentcontentimgin' src="{urls[currentkeys[0]]}">
                    </div>
                    <div class = 'contentimg{i}' id='contentimg'>
                        <img class = 'contentcontentimgin{i}' id='contentcontentimgin' src="{urls[currentkeys[1]]}">
                    </div>
                    <div class = 'contentimg{i}' id='contentimg'>
                        <img class = 'contentcontentimgin{i}' id='contentcontentimgin' src="{urls[currentkeys[2]]}">
                    </div>

                    <div class = 'contenttarget{i}' id='contenttarget'>
                        <span class="target{i}" id='target' data-accept{i}="{currentkeys[0]}">&nbsp;</span>
                    </div>
                    <div class = 'contenttarget{i}' id='contenttarget'>
                        <span class="target{i}" id='target' data-accept{i}="{currentkeys[1]}">&nbsp;</span>
                    </div>
                    <div class = 'contenttarget{i}' id='contenttarget'>
                        <span class="target{i}" id='target' data-accept{i}="{currentkeys[2]}">&nbsp;</span>
                    </div>
            """
            cnt = 0
            currentkeys = []
    if currentkeys != []:
        if len(currentkeys) == 2:
            span_str += f"""
                    <div class = 'contentimg{i}'>
                        <img class = 'contentcontentimgin{i}' id='contentcontentimgin' src="{urls[currentkeys[0]]}">
                    </div>
                    <div class = 'contentimg{i}'>
                        <img class = 'contentcontentimgin{i}' id='contentcontentimgin' src="{urls[currentkeys[1]]}">
                    </div>
                    <div>
                    </div>

                    <div class = 'contenttarget{i}' id='contenttarget'>
                        <span class="target{i}" id='target' data-accept{i}="{currentkeys[0]}">&nbsp;</span>
                    </div>
                    <div class = 'contenttarget{i}' id='contenttarget'>
                        <span class="target{i}" id='target' data-accept{i}="{currentkeys[1]}">&nbsp;</span>
                    </div>
                    <div>
                    </div>
            """
        elif len(currentkeys) == 1:
            span_str += f"""
                    <div class = 'contentimg{i}' id='contentimg'>
                        <img class = 'contentcontentimgin{i}' id='contentcontentimgin' src="{urls[currentkeys[0]]}">
                    </div>
                    <div>
                    </div>
                    <div>
                    </div>
                    <div class = 'contenttarget{i}' id='contenttarget'>
                        <span class="target{i}" id='target' data-accept{i}="{currentkeys[0]}">&nbsp;</span>
                    </div>
                    <div>
                    </div>
                    <div>
                    </div>

            """
    result += span_str
    result += f"""
                </div>

        </div>
        <button type="submit{i}" id='submitquizphoto' value="submit">Submit</button>

    </div>
    <script src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/208/h/99170efb96f914b9d28bac2931ae570f.js"></script>
    """+"""
    <script>
    """+f"""
            //initialize the quiz options
            var answersLeft{i} = [];
            $('.quiz-wrapper{i}').find('li.option{i}').each( function(i) """+"""{"""+f"""
                var $this{i} = $(this);
                var answerValue{i} = $this{i}.data('target{i}');
                var $target{i} = $('.answers{i} .target{i}[data-accept{i}="'+answerValue{i}+'"]');
                var labelText{i} = $this{i}.html();
                $this{i}.draggable( """+"""{"""+f"""
                    revert: "invalid",

                    stop: function(event, ui) """+"""{
                        """+f"""//$this{i}.css('color' ,'white');
                            $this{i}.css('border' ,'1px solid #F05C5C'); """+"""

                    }
                });
                """+f"""if ( $target{i}.length > 0 ) """+"""{"""+f"""
                    $target{i}.droppable( """+"""{

                    """+f"""accept: 'li.option{i}[data-target{i}="'+answerValue{i}+'"]',

                    drop: function( event, ui ) """+"""{"""+f"""
                        $this{i}.draggable('destroy');
                        $target{i}.droppable('destroy');
                        $this{i}.html('&nbsp;');
                        $target{i}.html(labelText{i});
                        answersLeft{i}.splice( answersLeft{i}.indexOf( answerValue{i} ), 1 );
                        $target{i}.css('border' ,'1px solid #5199FF');
                        $target{i}.css('background' ,'#E0ECFD');
                        $this{i}.css('background' ,'none');
                        $this{i}.css('display', 'none');
                        $target{i}.css('width','auto');
                        $target{i}.css('padding','2%');
                        if ( answersLeft{i}.length == 0 )"""+"""{"""+f"""
                            $('.options{i}').css('display','none');"""+"""
                            """+f"""
                            ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                            ans{i} = ans{i}-1;
                            $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                            if (ans{i} <= 0)"""+"""{"""+f"""
                                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                            }
                            """+"""
                        }
                    }
                });
                """+f"""answersLeft{i}.push(answerValue{i});"""+"""
                } else { }
            });

    </script>

    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_translate(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
    result = """<div id='quiz-wrapper-translate'>"""
    result += f"""<div class='textbck{i}' id='textbck'>
        <div class='textareadiv{i}' id='textareadiv'>
            <textarea class='textarea{i}' id='textarea' onfocus="if(this.value==this.defaultValue)this.value='';" onblur="if(this.value=='')this.value=this.defaultValue;">Начните писать перевод...
            </textarea>
        </div>
        <span>&nbsp;</span>
        <div class='translateddiv{i}' id='translateddiv'>
            <p class='translatedtext{i}' id='translatedtext'>{s}
            </p>
        </div>
        <div class='buttoncheck{i}' id='buttoncheck'>
            <img class='checkimg{i}' id='checkimg' src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/163/h/1d44da48d4e5127601c985d598e8dce6.svg">
            <button type="check{i}" id='checkquiztranslate' value="check{i}">Проверить</button>
        </div>
    </div>
    </div>

    <script>
        $('.textbck{i} button[type="check{i}"]').click( function() """+"""{"""+f"""
            if ($(".translateddiv{i}").css('display') == 'none')"""+"""{"""+f"""
                $(".translateddiv{i}").css('display','flex');
                $('.textbck{i} button[type="check{i}"]').html('Скрыть');"""+"""
                """+f"""
                ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                ans{i} = ans{i}-1;
                $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                if (ans{i} <= 0)"""+"""{"""+f"""
                    $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                    $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                }
                """+"""
            }
            else{"""+f"""
                $(".translateddiv{i}").css('display','none');
                $('.textbck{i} button[type="check{i}"]').html('Проверить');"""+"""
            }
        });
    </script>
    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_translate_new(s, galery_number, global_i, global_i_i):
    result_all = """"""

    s = s.split('\n')

    answers = []

    for el in s[2:]:
        answers.append(f'<p class="text-gray">{el.strip()}</p>')

    answers = '\n'.join(answers)

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
    result = f"""<div class="quiz-newtranslate-wrapper{i}" id="quiz-newtranslate-wrapper">
        <h1 class="goal">
            {s[0].strip()}
        </h1>
        <div class="translate">
            <textarea class='textarea' onfocus="if(this.value==this.defaultValue)this.value='';"
                onblur="if(this.value=='')this.value=this.defaultValue;">Начните писать перевод...</textarea>
            <br>
            <button onclick="newTranslateShowTranslationsDiv(this)">Проверить</button>
        </div>
        <div class="container hidden">
            <p class="answer"></p>
            <p class="text-gray">Один из вариантов перевода</p>
            <div class="translation">
                <h1>{s[1].strip()}</h1>
                <a onclick="newTranslateShowTranslations(this)">Все варианты перевода</a>
            </div>
            <div class="translations hidden">
                {answers}
            </div>
        </div>
    </div>
    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_audio_tts(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
    s = s.split('\n')
    textup = s[0].strip()
    textdown = s[1].strip()
    url = s[2].strip()
    words = url.split()
    url = 'https://api.voicerss.org/?key=602e84f5eaf14cfc8a980c3c1a661083&hl=en-us&v=Mike&с=mp3&f=16khz_16bit_mono&src='
    for w in words:
        url += w + '%20'
    # url = requests.get(url).text
    seekbar = bool(int(s[3]))
    audio, created = Audio.objects.get_or_create(
        text_up=textup,
        text_down=textdown,
        seekbar=seekbar,
        src=url,
        file=None,
    )
    if seekbar:
        seekbar = """
        <div>
                    <progress class="podcast-progress" id='podcast-progress' value="0" max="1"
                        onclick="audioTimeLineClick(this, event)"></progress>
                    <div class="f-container" id='f-container'>
                        <div class="podcast-time" id='podcast-time'>00:00 / 00:00</div>
                        <div class="podcast-speed" id='podcast-speed'>
                            <a class="podcast-speed-10 active" href="javascript:void(0)"
                                onclick="audioChangeSpeedClick(this)">1x</a> / <a class="podcast-speed-15"
                                href="javascript:void(0)" onclick="audioChangeSpeedClick(this)">1.5x</a> / <a
                                class="podcast-speed-20" href="javascript:void(0)"
                                onclick="audioChangeSpeedClick(this)">2x</a>
                        </div>
                    </div>
                </div>
        """
    else:
        seekbar = ""

    result = f"""
    <div class='audio-tts{audio.id} audio-div' id='audio-tts'>
            <audio class="audio-player{audio.id}" id='audio-player' src="{'https://'+ALLOWED_HOSTS[0]+audio.file.url.replace('media/', 'get-') if 'api.voicerss.org' in audio.src else audio.src}"
                onended="audioOnEnded(this)" oncanplay="audioOnCanPlay(this)" onplay="audioPlay(this)"
                onpause="audioPause(this)"></audio>
            <div class="podcast-container" id='podcast-container'>
                <div class="h-container" id='h-container'>
                    <div class="podcast-playpause" id='podcast-playpause'>
                        <img class="play" id="play"
                            src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/337/h/cb28b80bb66ad56d3c12fd1885bc3ef8.svg"
                            onclick="playPauseClick(this)">
                        <img class="pause" id="pause"
                            src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/197/h/7395c5433ab34099a1d5b9b139efdd5b.svg"
                            onclick="playPauseClick(this)">
                    </div>
                    <div>
                        <div class="podcast-title" id='podcast-title'>{audio.text_up}
                        <button type="button" onclick="audioSaveBtnClick(this)" id="{audio.id}"><i
                                    class="bi bi-bookmark-star"></i></button></div>
                        <div class="podcast-subtitle" id='podcast-subtitle'>{audio.text_down}</div>
                    </div>
                </div>

            </div>
            {seekbar}

        </div>
        """

    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_video(s, galery_number, global_i, global_i_i):
    result_all = """"""
    s = s.split("\n")
    poster = s[1]
    s = s[0]

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
    result = f"""    <video id='quizvideo' class='video{i}' src="{s}" poster="{poster}" controls></video>"""
    result += f"""
    <script>
        """+f"""
        $(function() """+"""{"""+f"""
            ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
            ans{i} = ans{i}-1;
            $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
            if (ans{i} <= 0)"""+"""{"""+f"""
                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                        $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
            }
        });
        """+"""
    </script>
    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiz6(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
    result = """"""
    word = s.split('\n')
    tr = word[1]
    word = word[0]
    wordarr = []
    wordkey = {}
    wordarrjs = ''
    j = 0
    for w in word:
        j += 1
        wordarrjs += "'"+w+"',"
        wordarr.append(w)
        wordkey[w] = j
    wordarrjs = wordarrjs[:-1]
    random.shuffle(wordarr)
    result += f"""
    <div class="quiz-wrapper{i}" id="quiz-wrapper-quiz6">
        <ul class="options{i}" id='options'>
    """
    for w in wordarr:
        result += f"""
            <li class="option{i}" id='option' data-target{i}="key_{i}_{wordkey[w]}">{w}</li>
            """
    result += f"""

        </ul>
        <div class="answers{i}" id='answers'>
            <div class ="general{i}" id='general'>
    """
    j = 0
    for w in word:
        j += 1
        result += f"""
                <div class = 'contenttarget{i}' id='contenttarget'>
                    <span class="target{i}" id='target' data-accept{i}="key_{i}_{j}">&nbsp;</span>
                </div>
                """

    result += f"""
            </div>
        </div>
        <div class="translatediv{i}" id='translatediv' style="display:none">
    """
    url = 'https://api.voicerss.org/?key=602e84f5eaf14cfc8a980c3c1a661083&hl=en-us&v=Mike&с=mp3&f=32khz_16bit_stereo&b64=true&src='
    url += word
    url = requests.get(url).text
    result += f"""
        <!-- ТУТ         \/ \/ \/-->
        <div class="audio-quiz6{i}" id='audio-quiz6'>
            <div>
                <div id='audio-buttons' >
                <img class="play" id="play" src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/337/h/cb28b80bb66ad56d3c12fd1885bc3ef8.svg" hspace="10" align="left">
                <img class="pause" id="pause" src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/197/h/7395c5433ab34099a1d5b9b139efdd5b.svg" hspace="10" align="left">
                    <audio class="player-quiz6_{i}" id="player" control="" hidden="false" preload="metadata" src="">
                    </audio>
                </div>

            </div>
            <div style="display:none">
                <span class="ct" id="ct" >00:00</span>
                <progress class="seekbar" id="seekbar" value="0" max="1"></progress>
                <span class="ft" id="ft">00:00</span>
                <hr style="display: inline-block">
            </div>
        </div>
        <span class="translatetext{i}" id='translatetext'>{tr}</span>
        </div>

    </div>
    """+"""
    <script src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/208/h/99170efb96f914b9d28bac2931ae570f.js"></script>

    """+"""
    <script>


    """+f"""
            //initialize the quiz options
            var word{i} = [{wordarrjs}];
            var iter{i} = 0;

            var answersLeft{i} = [];

            $('.option{i}').click( function() """+"""{"""+f"""
                if ($(this).html() == word{i}[iter{i}])"""+"""{"""+f"""
                    var key{i} = 'key_{i}_' + (iter{i}+1);
                    var $target{i} = $('.answers{i} .target{i}[data-accept{i}="'+key{i}+'"]');
                    $(this).html('&nbsp;');
                    $target{i}.html(word{i}[iter{i}]);
                    $target{i}.css('border' ,'1px solid #5199FF');
                    $target{i}.css('background' ,'#E0ECFD');
                    $(this).css('background' ,'none');
                    $(this).css('display', 'none');
                    $target{i}.css('padding' ,'7%');
                    iter{i}++;"""+"""
                }
                else{
                    //$(this).css('color' ,'#ed3a82');
                    $(this).css('border' ,'1px solid #F05C5C');
                }"""+f"""
                if (iter{i}>=word{i}.length)"""+"""{"""+f"""
                    //$('.quiz-wrapper{i} button[type="translate{i}"]').css('display','flex');
                    $('.translatediv{i}').css('display','flex');
                    $('.audio-quiz6{i}').css('display','flex');
                    """+f"""
                    ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                    ans{i} = ans{i}-1;
                    $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                    if (ans{i} <= 0)"""+"""{"""+f"""
                        $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                    $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                    }
                    """+f"""
                    $(".player-quiz6_{i}")[0].src = "{url}";
                    $(".player-quiz6_{i}")[0].load();"""+"""
                    jQuery(".play").click(function(){"""+f"""
                        $(this).nextAll(".player-quiz6_{i}").trigger("play");
                        $(this).css("display", "none");
                        $(this).next(".pause").css("display", "block");"""+"""
                    });
                    jQuery(".pause").click(function(){"""+f"""
                        $(this).nextAll(".player-quiz6_{i}").trigger("pause");
                        $(this).prev(".play").css("display", "block");
                        $(this).css("display", "none");"""+"""
                    });

                    //ТУТ

                    $('audio').on('ended', function(){
                        this.currentTime = 0;
                        $(this).prevAll(".pause").css("display", "none");
                        $(this).prevAll(".play").css("display", "block");
                    });
                }
            });


    </script>
    """

    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiz7(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    s = s.split('\n')
    ss = s[1]
    s = s[0]
    text_prev = ''
    text_next = ''
    key = ''
    check = 0
    for letter in s:
        if letter != '*' and check == 0:
            text_prev += letter
        elif letter == '*' and check == 0:
            check = 1
        elif letter != '*' and check == 1:
            key += letter
        elif letter == '*' and check == 1:
            check = 2
        elif letter != '*' and check == 2:
            text_next += letter
    ss = ss.split()
    ss.append(key)
    random.shuffle(ss)
    result = """"""
    result += f"""
    <div class="quiz-wrapper{i}" id='quiz-wrapper-quiz7'>
        <div class="answers{i}" id='answers'>
            <div class ="general{i}" id='general'>
                <div class = 'contenttargett{i}' id='contenttargett'>
                    <span id='contenttargettspan'>{text_prev}</span><span class="target{i}" id='target' data-accept{i}="key_{i}_100">&nbsp;</span>
                </div>
            </div>
        </div>
        <ul class="options{i}" id='options'>
    """
    j = 1
    r = """"""
    for el in ss:
        if el == key:
            r += f"""
                <li class="option{i}" id='option' data-target{i}="key_{i}_100">{el}</li>
            """
        else:
            r += f"""
                <li class="option{i}" id='option' data-target{i}="key_{i}_{j}">{el}</li>
            """
        j += 1
    result += r
    result += f"""
        </ul>
    </div>
    """+"""
    <script src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/208/h/99170efb96f914b9d28bac2931ae570f.js"></script>

    <script>

    """+f"""
            //initialize the quiz options
            var answersLeft{i} = [];
            $('.quiz-wrapper{i}').find('li.option{i}').each( function(i) """+"""{"""+f"""
                var $this{i} = $(this);
                var answerValue{i} = $this{i}.data('target{i}');
                var $target{i} = $('.answers{i} .target{i}[data-accept{i}="'+answerValue{i}+'"]');
                var labelText{i} = $this{i}.html();
                $this{i}.draggable( """+"""{"""+"""
                    revert: "invalid",

                    stop: function(event, ui) """+"""{
                        """+f"""//$this{i}.css('color' ,'white');
                            $this{i}.css('border' ,'1px solid #F05C5C'); """+"""

                    }
                });
                """+f"""if ( $target{i}.length > 0 ) """+"""{"""+f"""
                    $target{i}.droppable( """+"""{

                    """+f"""accept: 'li.option{i}[data-target{i}="'+answerValue{i}+'"]',

                    drop: function( event, ui ) """+"""{"""+f"""
                        $this{i}.draggable('destroy');
                        $target{i}.droppable('destroy');
                        $this{i}.html('&nbsp;');
                        $target{i}.html(labelText{i});
                        answersLeft{i}.splice( answersLeft{i}.indexOf( answerValue{i} ), 1 );
                        $target{i}.css('border' ,'1px solid #5199FF');
                        $target{i}.css('background' ,'#E0ECFD');
                        $this{i}.css('background' ,'none');
                        $this{i}.css('display', 'none');
                        if ( answersLeft{i}.length == 0 )"""+"""{"""+f"""
                            $('.options{i}').css('display','none');"""+"""
                            """+f"""
                            ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                            ans{i} = ans{i}-1;
                            $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                            if (ans{i} <= 0)"""+"""{"""+f"""
                                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                            }
                            """+"""
                        }
                    }
                });
                """+f"""answersLeft{i}.push(answerValue{i});"""+"""
                } else { }
            });
    </script>
    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quizOrder(s, galery_number, global_i, global_i_i):
    result_all = """"""

    result = """"""
    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    s = s.split('\n')
    while '' in s:
        s.pop(s.index(''))
    while ' ' in s:
        s.pop(s.index(' '))
    trueans = str(s)
    random.shuffle(s)
    li = """"""
    for el in s:
        if el != '' and el != ' ':
            li += f"""<li class="sortable-li-item{i}" id="sortable-li-item"><span>{el}</span></li>
            """
    result += f"""
    <div class='quizOrder{i}' id='quizOrder'>
        <ul class='sortable-ul-quizOrder{i}' id="sortable-ul-quizOrder">
            {li}
        </ul>
    </div>

    <script src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/208/h/99170efb96f914b9d28bac2931ae570f.js"></script>
    <script>
        $(function() """+"""{"""+f"""
            $( ".sortable-ul-quizOrder{i}" ).sortable("""+"""{"""+f"""
                revert: true,
                stop: function( event, ui )"""+"""{"""+f"""
                    checkItem{i}(getList{i}(),ui.item);"""+"""
                }
            });
            $( "#draggable" ).draggable({
                connectToSortable: "#sortable",
                helper: "clone",
                revert: "invalid"
            });"""+f"""
            $( "sortable-ul-quizOrder{i}, sortable-li-item{i}" ).disableSelection();"""+"""
        });
        """+f"""
        function getList{i}()"""+"""{"""+f"""
            var answers{i} = [];
            $('.quizOrder{i}').each(function()"""+"""{"""+f"""
                // inner scope
                var trueAnswers_i{i} = 0;
                var answer{i} = '';
                $(this).find('.sortable-li-item{i} span').each(function()"""+"""{"""+f"""
                    answer = '';
                    // cache jquery object
                    var current{i} = $(this);
                    // check for sub levels
                    if(current{i}.children().size() > 0) """+"""{"""+f"""
                        // check is sublevel is just empty UL
                        var emptyULtest = current{i}.children().eq(0);
                        if(emptyULtest.is('ul') && $.trim(emptyULtest.text())=="")"""+"""{"""+f"""
                            answer{i} += ' -BLANK- '; //custom blank text
                            return true;   """+"""
                        } else {
                            // else it is an actual sublevel with li's
                            return true;
                        }
                    }
                    """+f"""
                    answer{i} = current{i}.text();
                    if (answer{i}!='')"""+"""{"""+f"""
                        answers{i}.push(answer{i});"""+"""
                    }
                    """+f"""
                    trueAnswers_i{i}++;"""+"""
                });
            });
            """+f"""
            return answers{i}"""+"""
        }
        """+f"""
        function checkItem{i}(answers{i}, thisli{i})"""+"""{"""+f"""
            var trueAnswers{i} = {trueans};
            if (answers{i}.indexOf(thisli{i}.find('span').text()) != trueAnswers{i}.indexOf(thisli{i}.find('span').text()))"""+"""{"""+f"""
                thisli{i}.css('color' ,'#F05C5C');
                thisli{i}.find('span').css('color' ,'black'); """+"""
            }
            else{"""+f"""
                thisli{i}.css('color' ,'#5199FF');
                thisli{i}.find('span').css('color' ,'black'); """+"""
            }
            const equals = (a, b) =>
            a.length === b.length &&
                a.every((v, i) => v === b[i]);"""+f"""
            if (equals(getList{i}(),trueAnswers{i}))"""+"""{"""+f"""
                $('.quizOrder{i}').each(function()"""+"""{"""+f"""
                    $(this).find('.sortable-li-item{i}').each(function()"""+"""{"""+f"""
                        $(this).css('color' ,'#5199FF');
                        $(this).find('span').css('color' ,'black');"""+"""

                    });
                });
                """+f"""
                ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                ans{i} = ans{i}-1;
                $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                if (ans{i} <= 0)"""+"""{"""+f"""
                    $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                }
                """+"""
                """+f"""
                return answers{i}"""+"""
            }
            else{"""+f"""
                var trueAnswers{i} = {trueans};
                $('.quizOrder{i}').each(function()"""+"""{"""+f"""
                    $(this).find('.sortable-li-item{i}').each(function()"""+"""{
                        if ($(this).css('color') != 'rgb(193, 193, 193)'){"""+f"""
                            if (answers{i}.indexOf($(this).find('span').text()) != trueAnswers{i}.indexOf($(this).find('span').text()))"""+"""{
                                $(this).css('color' ,'#F05C5C');
                                $(this).find('span').css('color' ,'black');
                            }
                            else{
                                $(this).css('color' ,'#5199FF');
                                $(this).find('span').css('color' ,'black');
                            }
                        }

                    });
                });
            }

        }
    </script>
    """
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_stt(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
    result = """"""
    while s[-1] == '\n' or s[-1] == ' ':
        s = s[:-1]
    s += ' '
    s = s.upper()
    result += f"""
    <div class="container{i}" id='container-tts'>
        <p id='playbutton'>
            <button id='record{i}'><img id='rec' class='rec{i}' src='https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/186/h/bb3d9cc735d3db3636af1216341a995a.svg'></button>
        </p>
        <div style="display:none">
            Duration: <span id="duration">0ms</span>
        </div>
        <p style="display:none">
            <audio id="player" controls></audio>
        </p>
        <div class='loading{i}' id='loading'>
            <p class='loadingp{i}' id='loadingp'>Загрузка...</p>
        </div>
        <div class='resultdiv{i}' id='resultdiv'>
            <span class='resultspan{i}' id='resultspan'>Вы произнесли: </span><p class='result{i}' id='result'></p>
        </div>
        <div class='wrong{i}' id='wrong'>
            <p>Попробуйте еще раз</p>
        </div>

        <script>
            goal{i} = '{s}';
            function WzRecorder(config) """+"""{"""+f"""

                config = config || """+"""{}"""+f""";

                var self = this;
                var audioInput;
                var audioNode;
                var bufferSize = config.bufferSize || 4096;
                var recordedData = [];
                var recording = false;
                var recordingLength = 0;
                var startDate;
                var audioCtx;

                this.toggleRecording = function()"""+"""
                {"""+f"""
                    recording ? self.stop() : self.start();"""+"""
                }


                this.start = function() {"""+f"""
                    $(".rec{i}").attr("src", "https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/112/h/5574adb98dde5906ab787a483794a211.svg");
                    // reset any previous data
                    recordedData = [];
                    recordingLength = 0;

                    // webkit audio context shim
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();

                    if (audioCtx.createJavaScriptNode) """+"""{"""+f"""
                        audioNode = audioCtx.createJavaScriptNode(bufferSize, 1, 1);"""+"""
                    } """+f"""else if (audioCtx.createScriptProcessor) """+"""{"""+f"""
                        audioNode = audioCtx.createScriptProcessor(bufferSize, 1, 1);"""+"""
                    } else {
                        throw 'WebAudio not supported!';
                    }
                    """+f"""
                    audioNode.connect(audioCtx.destination);

                    """+"""
                    // Older browsers might not implement mediaDevices at all, so we set an empty object first
                    if (navigator.mediaDevices === undefined) {
                        navigator.mediaDevices = """+"""{}"""+""";
                    }

                    // Some browsers partially implement mediaDevices. We can't just assign an object
                    // with getUserMedia as it would overwrite existing properties.
                    // Here, we will just add the getUserMedia property if it's missing.
                    if (navigator.mediaDevices.getUserMedia === undefined) {
                        navigator.mediaDevices.getUserMedia = function(constraints) {

                            // First get ahold of the legacy getUserMedia, if present
                            var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

                            // Some browsers just don't implement it - return a rejected promise with an error
                            // to keep a consistent interface
                            if (!getUserMedia) {
                                return Promise.reject(new Error('getUserMedia is not implemented in this browser'));
                            }

                            // Otherwise, wrap the call to the old navigator.getUserMedia with a Promise
                            return new Promise(function(resolve, reject) {
                                getUserMedia.call(navigator, constraints, resolve, reject);
                            });
                        }
                    }


                    navigator.mediaDevices.getUserMedia({audio: true})
                    .then(onMicrophoneCaptured)
                    .catch(onMicrophoneError);
                };

                this.stop = function() {"""+f"""
                    $(".rec{i}").attr("src", "https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/186/h/bb3d9cc735d3db3636af1216341a995a.svg");

                    stopRecording(function(blob) """+"""{"""+f"""
                        self.blob = blob;
                        config.onRecordingStop && config.onRecordingStop(blob);"""+"""
                    });
                };
                """+"""
                this.upload = function (url, params, callback) {"""+f"""
                    var formData = new FormData();
                    formData.append("audio", self.blob, config.filename || 'recording.wav');

                    for (var i in params)
                        formData.append(i, params[i]);

                    var request = new XMLHttpRequest();
                    request.upload.addEventListener("progress", function (e) """+"""{"""+f"""
                        callback('progress', e, request);"""+"""
                    });"""+f"""
                    request.upload.addEventListener("load", function (e) """+"""{"""+f"""
                        callback('load', e, request);"""+"""
                    });
                    """+f"""
                    request.onreadystatechange = function (e) """+"""{"""+f"""
                        var status = 'loading';
                        if (request.readyState == 4)"""+"""
                        {"""+f"""
                            status = request.status == 200 ? 'done' : 'error';"""+"""
                        }
                        """+f"""
                        callback(status, e, request);"""+"""
                    };
                    """+f"""
                    request.open("POST", url);
                    request.send(formData);"""+"""
                };

                """+f"""
                function stopRecording(callback) """+"""{"""+f"""
                    // stop recording
                    recording = false;
                    """+"""
                    // to make sure onaudioprocess stops firing
                    window.localStream.getTracks().forEach( (track) => { track.stop(); });"""+f"""
                    audioInput.disconnect();
                    audioNode.disconnect();
                    """+"""
                    exportWav({"""+f"""
                        sampleRate: sampleRate,
                        recordingLength: recordingLength,
                        data: recordedData"""+"""
                    }, function(buffer, view) {"""+f"""
                        self.blob = new Blob([view],"""+""" { type: 'audio/wav' });"""+f"""
                        callback && callback(self.blob);"""+"""
                    });
                }

                """+"""
                function onMicrophoneCaptured(microphone) {
                """+f"""
                    if (config.visualizer)
                        visualize(microphone);

                    // save the stream so we can disconnect it when we're done
                    window.localStream = microphone;

                    audioInput = audioCtx.createMediaStreamSource(microphone);
                    audioInput.connect(audioNode);

                    audioNode.onaudioprocess = onAudioProcess;

                    recording = true;
                    self.startDate = new Date();

                    config.onRecordingStart && config.onRecordingStart();
                    sampleRate = audioCtx.sampleRate;"""+"""
                }

                function onMicrophoneError(e) {
                    console.log(e);
                    alert('Unable to access the microphone.');
                }

                function onAudioProcess(e) {"""+f"""
                    if (!recording) """+"""{"""+"""
                        return;
                    }
                    """+f"""
                    recordedData.push(new Float32Array(e.inputBuffer.getChannelData(0)));
                    recordingLength += bufferSize;
                    """+f"""
                    self.recordingLength = recordingLength;
                    self.duration = new Date().getTime() - self.startDate.getTime();
                    """+f"""
                    config.onRecording && config.onRecording(self.duration);"""+"""
                }


                function visualize(stream) {
                    var canvas = config.visualizer.element;
                    if (!canvas)
                        return;

                    var canvasCtx = canvas.getContext("2d");
                    var source = audioCtx.createMediaStreamSource(stream);

                    var analyser = audioCtx.createAnalyser();
                    analyser.fftSize = 2048;
                    var bufferLength = analyser.frequencyBinCount;
                    var dataArray = new Uint8Array(bufferLength);

                    source.connect(analyser);

                    function draw() {
                        // get the canvas dimensions
                        var width = canvas.width, height = canvas.height;

                        // ask the browser to schedule a redraw before the next repaint
                        requestAnimationFrame(draw);

                        // clear the canvas
                        canvasCtx.fillStyle = config.visualizer.backcolor || '#fff';
                        canvasCtx.fillRect(0, 0, width, height);

                        if (!recording)
                            return;

                        canvasCtx.lineWidth = config.visualizer.linewidth || 2;
                        canvasCtx.strokeStyle = config.visualizer.forecolor || '#f00';

                        canvasCtx.beginPath();

                        var sliceWidth = width * 1.0 / bufferLength;
                        var x = 0;


                        analyser.getByteTimeDomainData(dataArray);

                        for (var i = 0; i < bufferLength; i++) {

                            var v = dataArray[i] / 128.0;
                            var y = v * height / 2;

                            i == 0 ? canvasCtx.moveTo(x, y) : canvasCtx.lineTo(x, y);
                            x += sliceWidth;
                        }

                        canvasCtx.lineTo(canvas.width, canvas.height/2);
                        canvasCtx.stroke();
                    }

                    draw();
                }
                """+f"""
                function exportWav(config, callback) """+"""{"""+f"""
                    function inlineWebWorker(config, cb) """+"""{"""+f"""

                        var data = config.data.slice(0);
                        var sampleRate = config.sampleRate;
                        data = joinBuffers(data, config.recordingLength);

                        function joinBuffers(channelBuffer, count) """+"""{"""+f"""
                            var result = new Float64Array(count);
                            var offset = 0;
                            var lng = channelBuffer.length;

                            for (var i = 0; i < lng; i++) """+"""{"""+f"""
                                var buffer = channelBuffer[i];
                                result.set(buffer, offset);
                                offset += buffer.length;"""+"""
                            }
                            """+f"""
                            return result"""+""";
                        }
                        """+f""";
                        function writeUTFBytes(view, offset, string) """+"""{"""+f"""
                            var lng = string.length;
                            for (var i = 0; i < lng; i++) """+"""{"""+f"""
                                view.setUint8(offset + i, string.charCodeAt(i));"""+"""
                            }
                        }
                        """+f"""
                        var dataLength = data.length;

                        // create wav file
                        var buffer = new ArrayBuffer(44 + dataLength * 2);
                        var view = new DataView(buffer);

                        writeUTFBytes(view, 0, 'RIFF'); // RIFF chunk descriptor/identifier
                        view.setUint32(4, 44 + dataLength * 2, true); // RIFF chunk length
                        writeUTFBytes(view, 8, 'WAVE'); // RIFF type
                        writeUTFBytes(view, 12, 'fmt '); // format chunk identifier, FMT sub-chunk
                        view.setUint32(16, 16, true); // format chunk length
                        view.setUint16(20, 1, true); // sample format (raw)
                        view.setUint16(22, 1, true); // mono (1 channel)
                        view.setUint32(24, sampleRate, true); // sample rate
                        view.setUint32(28, sampleRate * 2, true); // byte rate (sample rate * block align)
                        view.setUint16(32, 2, true); // block align (channel count * bytes per sample)
                        view.setUint16(34, 16, true); // bits per sample
                        writeUTFBytes(view, 36, 'data'); // data sub-chunk identifier
                        view.setUint32(40, dataLength * 2, true); // data chunk length

                        // write the PCM samples
                        var index = 44;
                        for (var i = 0; i < dataLength; i++) """+"""{"""+f"""
                            view.setInt16(index, data[i] * 0x7FFF, true);
                            index += 2;"""+"""
                        }

                        if (cb) {
                            return cb({
                                buffer: buffer,
                                view: view
                            });
                        }

                        postMessage({
                            buffer: buffer,
                            view: view
                        });
                    }
                    """+f"""
                    var webWorker = processInWebWorker(inlineWebWorker);

                    webWorker.onmessage = function(event) """+"""{"""+f"""
                        callback(event.data.buffer, event.data.view);

                        // release memory
                        URL.revokeObjectURL(webWorker.workerURL);"""+"""
                    };
                    """+f"""
                    webWorker.postMessage(config);"""+"""
                }

                function processInWebWorker(_function) {"""+f"""
                    var workerURL = URL.createObjectURL(new Blob([_function.toString(),"""+"""
                                                                  ';this.onmessage = function (e) {' + _function.name + '(e.data);}'
                                                                 ], {
                                                                     type: 'application/javascript'
                                                                 }));
                    """+f"""
                    var worker = new Worker(workerURL);
                    worker.workerURL = workerURL;
                    return worker;"""+"""
                }
            }
        </script>
        <script>
        """+f"""
            var recorder = new WzRecorder("""+"""{
                onRecordingStop: function(blob) {
                    """+f"""
                    const form = new FormData();
                    form.append("sound", blob);
                    $('.loadingp{i}').html('Загрузка...');
                    $('.loading{i}').css('display','flex');
                    const settings = """+"""{
                        "async": true,
                        "crossDomain": true,
                        "url": "https://speech-recognition-english1.p.rapidapi.com/api/asr",
                        "method": "POST",
                        "headers": {
                            "x-rapidapi-host": "speech-recognition-english1.p.rapidapi.com",
                            "x-rapidapi-key": "c2587540d9msh64a8217c434399dp17580cjsn83f6e616938e"
                        },
                        "processData": false,
                        "contentType": false,
                        "mimeType": "multipart/form-data",
                        "data": form
                    };

                    $.ajax(settings).done(function (response) {
                        console.log(response);"""+f"""
                        var datajs = jQuery.parseJSON(response);
                        $('.result{i}').text(datajs.data.text.toString());
                        $('.loading{i}').css('display','none');
                        $('.resultdiv{i}').css('display','flex');
                        if ($('.result{i}').html()!=goal{i})"""+"""{"""+f"""
                            $('.result{i}').css('color','#ee5a5f');
                            $('.resultspan{i}').css('color','#ee5a5f');
                            $('.wrong{i}').css('display','flex');"""+"""
                        }
                        else{"""+f"""
                            $('.result{i}').css('color','#5cc3c2');
                            $('.resultspan{i}').css('color','#5cc3c2');
                            $('.wrong{i}').css('display','none');"""+"""
                            """+f"""
                            ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
                            ans{i} = ans{i}-1;
                            $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
                            if (ans{i} <= 0)"""+"""{"""+f"""
                                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
                                $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
                            }
                            """+"""
                        }
                    });
                    window.onerror = function(msg, url, linenumber) {
                            """+f"""$('.loadingp{i}').html('Речь не опознана, попробуйте ещё раз');"""+"""
                            return true;
                        }



                    console.log('Blob - ', blob);
                    """+f"""
                    var reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = function () """+"""{"""+f"""
                        var base64String = reader.result;"""+"""
                    }

                },
                onRecording: function(milliseconds) {
                    document.getElementById('duration').innerText = milliseconds + 'ms';
                }
            });
            """+f"""
            // wire up the microphone button to toggle recording
            document.getElementById('record{i}').onclick = recorder.toggleRecording;

        </script>
    </div>
        """

    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}

# def quizDialog(event):

#     global listbox_dialog
#     window_dialog_choose = tk.Tk()
#     window_dialog_choose.geometry('1280x720')
#     listbox_dialog = tk.Listbox(window_dialog_choose, height=20, width=20)
#     listbox_dialog.pack()
#     listbox_dialog.insert(tk.END, '')

#     listbox.insert(tk.END, 'Диалог')

#     button_left_dialog = tk.Button(window_dialog_choose, text='Слева',
#                                    width=25, height=5, command=lambda: quizDialog_input(event, 'слева'))
#     button_right_dialog = tk.Button(window_dialog_choose, text='Справа',
#                                     width=25, height=5, command=lambda: quizDialog_input(event, 'справа'))

#     button_left_dialog.pack()
#     button_right_dialog.pack()

#     window_dialog_choose.mainloop()


# def quizDialog_input(event, type):
#     global listbox_dialog

#     if type == 'слева':
#         listbox_dialog.insert(tk.END, 'Реплика слева')
#     else:
#         listbox_dialog.insert(tk.END, 'Реплика справа')

#     window_dialog_input = tk.Tk()
#     window_dialog_input.geometry('1280x720')
#     text_box_dialog_input = tk.Text(window_dialog_input)
#     text_box_dialog_input.insert(
#         "1.0", "Ссылка на картинку\nФраза для озвучки")
#     button_add_dialog_input = tk.Button(window_dialog_input, text=f'Добавить ({type})', width=25, height=5, command=lambda: pr_dialog(
#         event, text_box_dialog_input.get("1.0", tk.END), window_dialog_input, type))

#     text_box_dialog_input.pack()
#     button_add_dialog_input.pack()

#     window_dialog_input.mainloop()


# def pr_dialog(s, galery_number, global_i, global_i_i, type):

#     i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
#     result = """"""
#     s = s.split('\n')
#     url = s[1]
#     words = url.split()
#     url = 'https://api.voicerss.org/?key=602e84f5eaf14cfc8a980c3c1a661083&hl=en-us&v=Mike&с=mp3&f=32khz_16bit_stereo&b64=true&src='
#     for w in words:
#         url += w + '%20'
#     url = requests.get(url).text
#     url_to_svg = s[0]
#     url_for_audio = url
#     # display:flex;allign-items:center;
#     if type == 'справа':
#         type = 'right'
#         result += f"""
#         <div class="message{i}" id='messagetext_{type}' style=''>
#     <div class='audio-tts{i}' id='audio-ttsd' >
#     <audio class="audio-player{i}" id='audio-player' src=""></audio>
#     <div class="podcast-container" id='podcast-container'>
#         <div class="h-container" id='h-container'>
#             <div class="podcast-playpause" id='podcast-playpause'>
#                 <img class="play" id="play" src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/337/h/cb28b80bb66ad56d3c12fd1885bc3ef8.svg" hspace="10" align="left">
#                 <img class="pause" id="pause" src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/197/h/7395c5433ab34099a1d5b9b139efdd5b.svg" hspace="10" align="left">
#             </div>
#             <div>
#                 <div class="podcast-title" id='podcast-title'></div>
#                 <div class="podcast-subtitle" id='podcast-subtitle'></div>
#             </div>
#         </div>
#         <div style='display:none'>
#             <progress class="podcast-progress" id='podcast-progress' value="0" max="1"></progress>
#             <div class="f-container" id='f-container'>
#                 <div class="podcast-time" id='podcast-time'>00:00 / 00:00</div>
#                 <div class="podcast-speed" id='podcast-speed'>
#                     <a class="podcast-speed-10 active" href="javascript:void(0)">1x</a> / <a class="podcast-speed-15" href="javascript:void(0)">1.5x</a> / <a class="podcast-speed-20" href="javascript:void(0)">2x</a>
#                 </div>
#             </div>
#         </div>
#     </div>


# </div>
#     <script>
#         $(function()"""+"""{"""+f"""
#             ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
#             ans{i} = ans{i}-1;
#             $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
#             if (ans{i} <= 0)"""+"""{"""+f"""
#                 $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
#                         $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
#             }"""+f"""
#             $('.audio-tts{i} audio').on("canplay", function()"""+"""{"""+f"""
#                 $(this).parents().find('.audio-tts{i} .podcast-time').html(toHHMMSS(this.currentTime)+" / "+toHHMMSS(this.duration))"""+"""
#             });"""+f"""
#             $('.audio-tts{i} audio').on('ended', function()"""+"""{"""+f"""
#                 if($('.audio-tts{i} .podcast-playpause').hasClass('playing')) """+"""{"""+f"""
#                     $('.audio-tts{i} .podcast-playpause').removeClass('playing');"""+"""
#                 }"""+f"""
#                 $(".audio-tts{i} .audio-player{i}").stop();
#                 $('.audio-tts{i} .pause').hide();
#                 $('.audio-tts{i} .play').show();"""+"""
#             });"""+f"""
#             $('.audio-tts{i} .podcast-playpause').on('click', function()"""+""" {"""+f"""
#                 $(".audio-tts{i} .audio-player{i}")[0].src = "{url_for_audio}";
#                 $(".audio-tts{i} .audio-player{i}")[0].load();
#                 let that = this;
#                 let audio = $(this).parents().find('.audio-tts{i} .audio-player{i}').get(0);
#                 if($(this).hasClass('playing')) """+"""{"""+f"""
#                     $(this).removeClass('playing');
#                     audio.pause();
#                     $('.audio-tts{i} .pause').hide();
#                     $('.audio-tts{i} .play').show();
#                     $(audio).off('timeupdate');"""+"""
#                 } else {"""+f"""
#                     $(this).addClass('playing');
#                     audio.play();
#                     $('.audio-tts{i} .pause').show();
#                     $('.audio-tts{i} .play').hide();
#                     $(audio).on('timeupdate', function() """+"""{ """+f"""
#                         $(that).parents().find('.audio-tts{i} .podcast-progress').attr("value", this.currentTime / this.duration);
#                         $(that).parents().find('.audio-tts{i} .podcast-time').html(toHHMMSS(this.currentTime)+" / "+toHHMMSS(this.duration))"""+"""
#                     });
#                 }
#             });"""+f"""
#             $('.audio-tts{i} .podcast-speed a').on('click', function()"""+""" {"""+f"""
#                 $(this).siblings().removeClass('active');
#                 $(this).addClass('active');
#                 let audio = $(this).parents().find('.audio-tts{i} .audio-player{i}').get(0);"""+"""
#                 if($(this).hasClass('podcast-speed-10')) {
#                     audio.playbackRate=1;
#                 }
#                 else if($(this).hasClass('podcast-speed-15')) {
#                     audio.playbackRate=1.5;
#                 }
#                 else if($(this).hasClass('podcast-speed-20')) {
#                     audio.playbackRate=2;
#                 }
#             });"""+f"""
#             $('.audio-tts{i} .podcast-progress').on('click', function(e) """+"""{ console.log(this.offsetWidth)"""+f"""
#             let audio = $(this).parents().find('.audio-tts{i} .audio-player{i}').get(0);
#                                                                         var percent = e.offsetX / this.offsetWidth;
#                                                                         audio.currentTime = percent * audio.duration;
#                                                                         $(this).val(percent);
#                                                                         $(this).parents().find('.audio-tts{i}.podcast-time').html(toHHMMSS(audio.currentTime)+" / "+toHHMMSS(audio.duration))
#                                                                         """+"""
#                                                                         });
#         });

#         function toHHMMSS(sec) {
#             var sec_num = parseInt(sec, 10);
#             var hours   = Math.floor(sec_num / 3600);
#             var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
#             var seconds = sec_num - (hours * 3600) - (minutes * 60);

#             if (hours   < 10) {hours   = "0"+hours;}
#             if (minutes < 10) {minutes = "0"+minutes;}
#             if (seconds < 10) {seconds = "0"+seconds;}
#             return hours == "00" ? minutes+':'+seconds : hours+':'+minutes+':'+seconds;
#         }
#     </script> """ + f"""

#     <img class="mentor" id="textmentor_{type}" src="{url_to_svg}" >
#     </div>
#     """

#     else:
#         type = 'left'
#         result += f"""<div class="message{i}" id='messagetext_{type}' style=''>
#     <img class="mentor" id="textmentor_{type}" src="{url_to_svg}" >
#     """ + f"""
#     <div class='audio-tts{i}' id='audio-ttsd' >
#     <audio class="audio-player{i}" id='audio-player' src=""></audio>
#     <div class="podcast-container" id='podcast-container'>
#         <div class="h-container" id='h-container'>
#             <div class="podcast-playpause" id='podcast-playpause'>
#                 <img class="play" id="play" src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/337/h/cb28b80bb66ad56d3c12fd1885bc3ef8.svg" hspace="10" align="left">
#                 <img class="pause" id="pause" src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/197/h/7395c5433ab34099a1d5b9b139efdd5b.svg" hspace="10" align="left">
#             </div>
#             <div>
#                 <div class="podcast-title" id='podcast-title'></div>
#                 <div class="podcast-subtitle" id='podcast-subtitle'></div>
#             </div>
#         </div>
#         <div style='display:none'>
#             <progress class="podcast-progress" id='podcast-progress' value="0" max="1"></progress>
#             <div class="f-container" id='f-container'>
#                 <div class="podcast-time" id='podcast-time'>00:00 / 00:00</div>
#                 <div class="podcast-speed" id='podcast-speed'>
#                     <a class="podcast-speed-10 active" href="javascript:void(0)">1x</a> / <a class="podcast-speed-15" href="javascript:void(0)">1.5x</a> / <a class="podcast-speed-20" href="javascript:void(0)">2x</a>
#                 </div>
#             </div>
#         </div>
#     </div>


# </div>
#     <script>
#         $(function()"""+"""{"""+f"""
#             ans{i} = parseInt($(".checkans{str(galery_number)}_{str(global_i)}").html());
#             ans{i} = ans{i}-1;
#             $(".checkans{str(galery_number)+'_'+str(global_i)}").html(ans{i}.toString());
#             if (ans{i} <= 0)"""+"""{"""+f"""
#                 $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#5199FF');
#                         $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('1');"""+"""
#             }"""+f"""
#             $('.audio-tts{i} audio').on("canplay", function()"""+"""{"""+f"""
#                 $(this).parents().find('.audio-tts{i} .podcast-time').html(toHHMMSS(this.currentTime)+" / "+toHHMMSS(this.duration))"""+"""
#             });"""+f"""
#             $('.audio-tts{i} audio').on('ended', function()"""+"""{"""+f"""
#                 if($('.audio-tts{i} .podcast-playpause').hasClass('playing')) """+"""{"""+f"""
#                     $('.audio-tts{i} .podcast-playpause').removeClass('playing');"""+"""
#                 }"""+f"""
#                 $(".audio-tts{i} .audio-player{i}").stop();
#                 $('.audio-tts{i} .pause').hide();
#                 $('.audio-tts{i} .play').show();"""+"""
#             });"""+f"""
#             $('.audio-tts{i} .podcast-playpause').on('click', function()"""+""" {"""+f"""
#                 $(".audio-tts{i} .audio-player{i}")[0].src = "{url_for_audio}";
#                 $(".audio-tts{i} .audio-player{i}")[0].load();
#                 let that = this;
#                 let audio = $(this).parents().find('.audio-tts{i} .audio-player{i}').get(0);
#                 if($(this).hasClass('playing')) """+"""{"""+f"""
#                     $(this).removeClass('playing');
#                     audio.pause();
#                     $('.audio-tts{i} .pause').hide();
#                     $('.audio-tts{i} .play').show();
#                     $(audio).off('timeupdate');"""+"""
#                 } else {"""+f"""
#                     $(this).addClass('playing');
#                     audio.play();
#                     $('.audio-tts{i} .pause').show();
#                     $('.audio-tts{i} .play').hide();
#                     $(audio).on('timeupdate', function() """+"""{ """+f"""
#                         $(that).parents().find('.audio-tts{i} .podcast-progress').attr("value", this.currentTime / this.duration);
#                         $(that).parents().find('.audio-tts{i} .podcast-time').html(toHHMMSS(this.currentTime)+" / "+toHHMMSS(this.duration))"""+"""
#                     });
#                 }
#             });"""+f"""
#             $('.audio-tts{i} .podcast-speed a').on('click', function()"""+""" {"""+f"""
#                 $(this).siblings().removeClass('active');
#                 $(this).addClass('active');
#                 let audio = $(this).parents().find('.audio-tts{i} .audio-player{i}').get(0);"""+"""
#                 if($(this).hasClass('podcast-speed-10')) {
#                     audio.playbackRate=1;
#                 }
#                 else if($(this).hasClass('podcast-speed-15')) {
#                     audio.playbackRate=1.5;
#                 }
#                 else if($(this).hasClass('podcast-speed-20')) {
#                     audio.playbackRate=2;
#                 }
#             });"""+f"""
#             $('.audio-tts{i} .podcast-progress').on('click', function(e) """+"""{ console.log(this.offsetWidth)"""+f"""
#             let audio = $(this).parents().find('.audio-tts{i} .audio-player{i}').get(0);
#                                                                         var percent = e.offsetX / this.offsetWidth;
#                                                                         audio.currentTime = percent * audio.duration;
#                                                                         $(this).val(percent);
#                                                                         $(this).parents().find('.audio-tts{i}.podcast-time').html(toHHMMSS(audio.currentTime)+" / "+toHHMMSS(audio.duration))
#                                                                         """+"""
#                                                                         });
#         });

#         function toHHMMSS(sec) {
#             var sec_num = parseInt(sec, 10);
#             var hours   = Math.floor(sec_num / 3600);
#             var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
#             var seconds = sec_num - (hours * 3600) - (minutes * 60);

#             if (hours   < 10) {hours   = "0"+hours;}
#             if (minutes < 10) {minutes = "0"+minutes;}
#             if (seconds < 10) {seconds = "0"+seconds;}
#             return hours == "00" ? minutes+':'+seconds : hours+':'+minutes+':'+seconds;
#         }
#     </script>
#     </div>
#     """

#     result_all += result
#     global_i_i += 1


def pr_quiz8(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    result = """"""
    result += f"""
    <div class="quiz-wrapper{i}" id="quiz-wrapper-quiz8">
    """
    words = s.split('\n')
    cnt = 1
    for el in words:
        el = "<span>" + el.strip('\n').strip() + "</span>"
        if el:
            while "..." in el:
                el = el.replace(
                    "...",
                    f'<input type="text" class="input" id="input{cnt}" quiz-uuid="{str(uuid.uuid4())}" oninput="getInputQuiz8(this)" onchange="checkAnswerQuiz8(this)" trueanswer="',
                    1
                )
                el = el.replace(
                    "...", f'"><div class="input-buffer" id="input{cnt}-buffer"></div>', 1)
                cnt += 1
            el += '\n<br>\n'
            result += el

    result += '\n<button class="setAnswer" onclick="setAnswerQuiz8(this)">Подсказка</button>'

    result += f"""
        </div>

    """

    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiztable(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    result = """"""
    result += f"""
    <div class="quiz-wrapper{i}" id="quiz-wrapper-table" quiz-uuid="{str(uuid.uuid4())}">
    """
    s = s.split('\n')
    zagz = []
    words = []
    for line in s:
        if line:
            if line.endswith(':'):
                zagz.append(line.rstrip(':'))
            else:

                line = line.split(';')
                for word in line:
                    word = f'<li class="option{len(zagz)}{i}" id="option">{word}</li>'
                    words.append(word)

    random.shuffle(words)
    result += f"""
        <div class="option-wrapper">
        <ul class="options mostly-customized-scrollbar nowrap" id="options">
        """
    for el in words:
        result += f"""
        {el}
        """
    result += f"""
    </ul>
        <img class="show-all" onclick="showAllQuizTable(this)" src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/52/h/986a4fca44344a5651049312fce6e607.svg">
    </div>
    <div class="col-headers">
        <div class="col1-header" id="col-header">
            Заголовок1
        </div>
        <div class="col1-header" id="col-header">
            Заголовок2
        </div>
        <div class="col1-header" id="col-header">
            Заголовок3
        </div>
    </div>
    <div class="quiz-table" id="quiz-table">
        <div class="table-col1" id="table-col">
            <div class="col-items col-left" id="col-items1">
                <ul id="target1{i}">
                    <li>&nbsp;</li>
                </ul>
            </div>
        </div>
        <div class="table-col2" id="table-col">
            <div class="col-items col-center" id="col-items2">
                <ul id="target2{i}">
                    <li>&nbsp;</li>
                </ul>
            </div>
        </div>
        <div class="table-col3" id="table-col">
            <div class="col-items col-right" id="col-items3">
                <ul id="target3{i}">
                    <li>&nbsp;</li>
                </ul>
            </div>
        </div>
    </div>
        </div>

    """

    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_quiz9(s, galery_number, global_i, global_i_i):
    result_all = """"""

    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)
    import random
    import requests
    words = s.split('\n')
    quizType = words.pop(0).strip()
    descr = words.pop(0).strip()
    result = """"""
    result += f"""
    <div class="type{quizType} quiz-wrapper{i}" id="quiz9-wrapper" quiz-uuid="{str(uuid.uuid4())}">
        <ul>
    """
    cnt = 1
    for el in words:
        if el:
            true = ""
            el = el.strip("\n")
            if el.endswith('*'):
                true = "true"

                el = el.rstrip("*")

            el = el.strip()
            result += f"""<li><button onclick="checkQuiz9(this)" {f'descr="{descr}"' if not true and descr else ""} {true}>{el}</button></li>"""
            result += "\n"

    result += '\n</ul>'

    result += f"""
    </div>
    """

    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_textAudio(s, galery_number, global_i, global_i_i):
    result_all = """"""
    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    result = """"""
    result += f"""
    <div class="text-audio-div-wrapper">
    """
    s: List[str] = s.split('\n')
    for el in s:
        if el.strip() == '':
            result += '<br>\n'
        else:
            url = re.search(r'<<.*>>', el).group(0)[2:-2]
            text = re.search(r'.*<<', el).group(0)[:-2].strip()
            if url:
                result += f"""
             <audio class='audio-player' id='audio-player' src="{url}"
                onended="textAudioOnEnded(this)" oncanplay="textAudioOnCanPlay(this)" onplay="textAudioPlay(this)"
                onpause="textAudioPause(this)">
            </audio>
            """
            result += f"""
            <span class="text">
                <span class="podcast-title">{text}</span>
                <i class="play bi bi-play-circle-fill" id="play" onclick="textAudioPlayPauseClick(this)"></i>
                <i class="pause bi bi-pause-circle-fill" id="pause" onclick="textAudioPlayPauseClick(this)"></i>
            </span>
            """
    result += "</div>"
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def pr_dropdownQuiz(s, galery_number, global_i, global_i_i):
    result_all = """"""
    i = str(galery_number)+'_'+str(global_i)+'_'+str(global_i_i)

    result = """"""
    result += f"""
        <div>
    """

    def repl1(match):
        match = match.group(0)
        return f"""
            <span>{match}</span>
        """

    def repl(match):
        match = match.group(0)[2:-2]
        match = match.split(';')
        print(f"{len(match)=}")
        if len(match) == 1:

            return f"""<div class="dropdown">
                        <button class="btn dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown"
                            aria-haspopup="true" aria-expanded="false">
                            ___
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton"
                            quiz-uuid="{uuid.uuid4()}">
                            <input type="text" trueanswer="{match[0]}">
                            <button class="btn" onclick="setAnswerDropwownInput(this)">✓</button>
                        </div>
                    </div>
                    """
        else:
            btns = [
                f"""<button type="button" class="dropdown-item" {"true" if i == 0 else ""} onclick="setAnswerDropwown(this)">{el}</button>"""
                for i, el in enumerate(match)
            ]

            random.shuffle(btns)
            btns = '\n'.join(btns)
            return f"""<div class="dropdown">
                        <button class="btn dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown"
                            aria-haspopup="true" aria-expanded="false">
                            ___
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton"
                            quiz-uuid="{uuid.uuid4()}">
                            {btns}
                        </div>
                    </div>
                    """

    s: List[str] = s.split('\n')
    for el in s:
        if el.strip() == '':
            result += '<br>\n'
        else:
            result += '<div class="dropdown-wrapper">\n'
            el = re.sub(r"(?<!<<)[\w\s.,!?-]+(?![^<>]*>>)", repl1, el)
            el = re.sub(r"<<.*>>", repl, el)
            result += el
            result += '</div>\n'

    result += "</div>"
    result_all += result
    global_i_i += 1
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def nextslide(galery_number, global_i, global_i_i):
    result_all = """"""
    global_i += 1

    # listbox.insert(tk.END, f'{global_i} слайд') # ДОБАВИТЬ

    result_all += f"""\n</div>
        <p class='checkans{str(galery_number)+'_'+str(global_i-1)}' style='display:none;'>{global_i_i-1}</p>\n"""
    result_all += f"""<div class='galery_div{str(galery_number)+'_'+str(global_i)}' style = "display:none;">\n"""
    global_i_i = 1
    # messagebox.showinfo("Инфо", "Успешно создан слайд!") # ДОБАВИТЬ
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def end(ifNextBtn, galery_number, global_i, global_i_i):
    result_all = """"""
    if ifNextBtn == "1":
        displaynext = "style='display:none'"
    else:
        displaynext = ''

    result_all += f"""\n</div>\n<p class='checkans{str(galery_number)+'_'+str(global_i)}' style='display:none;'>{global_i_i-1}</p>\n"""
    result_all += f"""<div class='buttonnext_{str(galery_number)}' id='buttonnextdiv' {displaynext}>
                <button type="next_{str(galery_number)}" id='buttonnext' value="0">Далее</button>
            </div>\n"""

    result_all += f"""
        <div id='divgaleryresult' class='divgaleryresult{str(galery_number)}'>
            <p id='galeryresult' class='galeryresult{str(galery_number)}'>Вы успешно выполнили задания!</p>
            <button type='galeryreload{str(galery_number)}' id='galeryreload' onclick='document.location.reload(true)'>Начать заново</button>
        </div>
        """
    result_all += f"""<script>
    var i_{galery_number} = 1;
    var lasti_{galery_number} = {global_i+1};

    $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').click( function() """+"""{"""+f"""
        if ($('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val() == '1')"""+"""{"""+f"""
            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').val('0');
            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('background','#a0a0a0');
            var curdiv = '.galery_div{str(galery_number)}_' + i_{galery_number}.toString();
            var nextdiv = '.galery_div{str(galery_number)}_' + (i_{galery_number}+1).toString();
            i_{galery_number}++;
            $(curdiv).css('display','none');
            $(nextdiv).css('display','block');"""+f"""

            if (i_{galery_number}==lasti_{galery_number})"""+"""{""" + f"""
            $('.galery{str(galery_number)} button[type="next_{str(galery_number)}"]').css('display','none');
            $('.divgaleryresult{str(galery_number)}').css('display','flex');
            """+"""
            }
        }
    });

    </script>"""+f"""
    </div>\n
    """
    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}


def start(galery_number, global_i, global_i_i):
    result_all = """"""
    result_all += f"""<div class='galery{str(galery_number)}' id='galery'>\n"""
    result_all += f"""<div class='galery_div{str(galery_number)+'_'+str(global_i)}' id='galerydiv'>\n"""

    return {"s": result_all, "galery_number": galery_number, "global_i": global_i, "global_i_i": global_i_i}
