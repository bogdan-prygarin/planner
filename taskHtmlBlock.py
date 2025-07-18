    

def open(tasksArr):
    returnStr = ''
    
    for i in tasksArr:
        returnStr += f'''
        <div class="task">
                <div class="task-details">
                    <h2>{i[1]}</h2>
                </div>
                <div class="task-time">
                    <span class="time">{i[2]}</span>
                    <span class="timer">{i[3]}</span>
                </div>
            </div>
        '''
    return returnStr