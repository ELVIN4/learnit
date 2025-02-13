
// Инициализация редактора
var quill = new Quill('#editor', {
    theme: 'snow',
    modules: {
      toolbar: [
        ['bold', 'italic', 'underline'],   // Оставляем только базовые инструменты
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'header': [1, 2, false] }],
        ['link']
      ]
    }
  });
  
var videoId = document.getElementById('video-container').getAttribute('data-video-id');


// Загружаем сохраненные данные из localStorage
var savedContent = localStorage.getItem('noteContent_' + videoId);
if (savedContent) {
  quill.root.innerHTML = savedContent;
}
else {
    quill.root.innerHTML = "Take notes here, and they'll be stored for later...";
}
// Сохраняем в localStorage при каждом изменении
quill.on('text-change', function() {
  var content = quill.root.innerHTML;
  localStorage.setItem('noteContent_' + videoId, content);
});

