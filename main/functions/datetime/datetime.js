// datetime.js

// 曜日の配列
const daysOfWeekJp = ['日', '月', '火', '水', '木', '金', '土'];
const daysOfWeekEn = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const daysOfWeekEnShort = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

// 指定されたフォーマットで日付と時刻を取得する関数
function getFormattedDate(format) {
    const now = new Date();
    const padZero = (num) => num.toString().padStart(2, '0');
    
    let formattedDate = format
        .replace('YYYY', now.getFullYear())
        .replace('YY', padZero(now.getFullYear() % 100))
        .replace('MM', padZero(now.getMonth() + 1))
        .replace('DD', padZero(now.getDate()))
        .replace('hh', padZero(now.getHours()))
        .replace('mm', padZero(now.getMinutes()))
        .replace('ss', padZero(now.getSeconds()))
        .replace('dowes', daysOfWeekEnShort[now.getDay()])
        .replace('dowe', daysOfWeekEn[now.getDay()])
        .replace('dowj', daysOfWeekJp[now.getDay()])
        .replace('dow', now.getDay() + 1)
        ;
    return formattedDate;
}

// 時計を指定されたIDのdivに表示する関数
function updateClock(format) {
    const clockElement = document.getElementById(`txt_datetime_${format}`);
    if (clockElement) {
        clockElement.innerText = getFormattedDate(format);
    }
}

// 自動更新を設定する関数
function startClockUpdate(format, interval = 1000) {
    updateClock(format); // 最初に一度表示を更新
    setInterval(() => updateClock(format), interval); // 指定された間隔で更新
};

