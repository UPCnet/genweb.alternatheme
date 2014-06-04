
module.exports = function (grunt) {
    'use strict';

    grunt.initConfig({
        less: {
            genwebupc: {
                options: {
                  paths: ['genweb/alternatheme/components/bootstrap/less'],
                  strictMath: false,
                  sourceMap: true,
                  outputSourceFiles: true,
                  sourceMapURL: '/++gw++stylesheets/genwebupc.css.map',
                  sourceMapFilename: 'genweb/alternatheme/stylesheets/genwebupc.css.map'
                },
                files: {
                  'genweb/alternatheme/stylesheets/genwebupc.css': 'genweb/alternatheme/less/genwebupc.less'
                }
            },
        },
        watch: {
            scripts: {
                files: ['genweb/alternatheme/less/*.less'],
                tasks: ['less']
            }
        },
        bless: {
            css: {
              options: {},
              files: {
                'genweb/alternatheme/stylesheets/genwebupc-ie.css': 'genweb/alternatheme/stylesheets/genwebupc.css'
              }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-bless');
    grunt.registerTask('default', ['less']);
};
