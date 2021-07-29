// In your Javascript (external .js resource or <script> tag)
$(document).ready(function() {
  var resposta_certa=document.getElementById('valor_geral')
  $('.js-data-example-ajax').select2({
  minimumInputLength: 2,
  placeholder: 'Search',
  ajax: {
    url: "/rota_jason",
    dataType: 'json',
    delay: 250,
        
    // Additional AJAX parameters go here; see the end of this chapter for the full code of this example
  }
});
  $('.js-data-example-ajax').on('select2:select', function (e) {
    var data = e.params.data;
    value= $('.js-data-example-ajax').select2('data');
    var value3=''
    for(var i=0 in value) {
      value3+=value[i].text+',';
      }
    fetch('/rota_escolha/' + value3).then(function(response) {
      response.json().then(function(data){
         resposta_certa.innerHTML=data.item2;   
      });
        });
});

  $('.js-data-example-ajax').on('select2:unselect', function (e) {
    var data = e.params.data;
    value= $('.js-data-example-ajax').select2('data');
    var value3=''
    for(var i=0 in value) {
      value3+=value[i].text+',';
      }
    fetch('/rota_escolha/' + value3).then(function(response) {
        response.json().then(function(data){
         resposta_certa.innerHTML=data.item2;   
          });
        });
});
});

