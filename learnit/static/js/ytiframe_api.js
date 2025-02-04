// Загрузка IFrame Player API асинхронно
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// Функция для сохранения текущего состояния плеера и возврата на него
var player;
var videoId = document.getElementById('video-container').getAttribute('data-video-id');

function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '360',
    width: '640',
    videoId: videoId,
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

// Устанавливаем время из localStorage при загрузке страницы
function onPlayerReady(event) {
  var savedTime = localStorage.getItem(videoId);
  if (savedTime) {
    player.seekTo(+savedTime);
  }
}

// Сохраняем текущее время каждые 1 секунду, но не устанавливаем его
function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PLAYING) {
    setInterval(() => {
      var seconds = Math.round(player.getCurrentTime());
      localStorage.setItem(videoId, seconds);
    }, 1000);
  }
}
