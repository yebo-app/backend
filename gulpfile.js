'use strict';

var gulp = require('gulp');
var browserSync 	 = require('browser-sync').create();
var exec = require('child_process').exec;
exec('python manage.py runserver');

gulp.task('browser-sync', function(done) {
  browserSync.init({
    notify: false,
    port: 8000,
    proxy: 'localhost:8000'
  });

  browserSync.watch('yearbook/templates/yearbook/*.html').on('change', browserSync.reload);

  done()
});



// gulp.task('watch',function() {
//     gulp.watch('./sass/**/*.scss', gulp.series('sass'));
// });

gulp.task('watch', gulp.series('browser-sync', function(done) {
  
    
  done()
}));