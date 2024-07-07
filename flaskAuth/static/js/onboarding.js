$(function() {
    let $step1 = $('.wrap').eq(0);
    let $step2 = $('.wrap').eq(1);
    let $step3 = $('.wrap').eq(2);
    let $content = $('#content');
    let $thanks = $('#content-thanks');
    let $dashboard = $('#content-dashboard');
    let countrySelected = false;
    
    // select2 hook
    $('.select2-selects').select2();
  
    function setFirstBtn() {
      let  $checks = $step1.find('.ga-checkbox');
      if (countrySelected && $step1.find('.ga-checkbox:checked').length == $checks.length) {
         $step1.find('.btn-first').prop('disabled', false);
      } else {
        $step1.find('.btn-first').prop('disabled', true);
      }
    }
  
    // enable on select change
    $step1.find('.select-country').change(function(e) {
      countrySelected = true
      setFirstBtn()
    });
  
    $step1.find('.ga-checkbox').eq(0).change(function(e) {
      setFirstBtn()
    });
  
    $step1.find('.ga-checkbox').eq(1).change(function(e) {
      setFirstBtn()
    });
  
    // hide all
    $('.wrap').addClass('hidden');
  
    // open first
    $step1.removeClass('hidden');
  
    // on step 1 button continue
    $step1.find('.click').click(function(e) {
      $step1.addClass('hidden');
      $step2.removeClass('hidden');
  
      // check off
      $step1.addClass('complete').find('.state-icon').text('');
    });
  
    // on step 2 button continue
    $step2.find('.click').click(function(e) {
      $step2.addClass('hidden');
      $step3.removeClass('hidden');
  
      // check off
      $step2.addClass('complete').find('.state-icon').text('');
    });
  
    // on step 3 button continue
    $step3.find('.click').click(function(e) {
      $content.hide();
      $thanks.fadeIn();
      
      // set timer for 2s and show dashboard
      setTimeout(function() {
        $dashboard.fadeIn();
        $thanks.hide();
      }, 2000)
    });
  });
  