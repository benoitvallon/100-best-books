$(document).ready(function() {
  $('#bs-example-navbar-collapse-1').on('show.bs.collapse', function () {
    var heightLimit = 30,
        height = $(window).scrollTop();

    if(height <= heightLimit) {
      $('.navbar').removeClass('navbar-transparent');
    }
  });

  $('#bs-example-navbar-collapse-1').on('hide.bs.collapse', function () {
    var heightLimit = 30,
        height = $(window).scrollTop();

    if(height <= heightLimit) {
      $('.navbar').addClass('navbar-transparent');
    }
  });

  $(window).scroll(function () {
    var heightLimit = 30,
        height = $(window).scrollTop();
        navbarCollapsed = $('.navbar-collapse.in').length;

    if(!navbarCollapsed) {
      if(height > heightLimit) {
        $('.navbar').removeClass('navbar-transparent');
      } else {
        $('.navbar').addClass('navbar-transparent');
      }
    }
  });
});
