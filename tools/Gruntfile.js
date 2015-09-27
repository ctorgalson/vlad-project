/**
 * @file
 * Used to auto-run `vagrant rsync` in cases where `vagrant rsync-auto` does not
 * work as intended.
 */
module.exports = function(grunt) {
  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    vagrantPath: "vlad",
    vladProject: grunt.file.readYAML("settings/vlad_settings.yml"),

    // Watch filesystem.
    watch: {
      src: {
        files: [
          // By default, watch all files in docroot.
          "<%= vladProject.host_synced_folder.slice(3) %>/**/*"
        ],
        tasks: "shell:vagrant_rsync"
      }
    },

    // Shell tasks.
    shell: {
      // Run `cd vlad && vagrant rsync` on filesystem changes.
      vagrant_rsync: {
        command: "cd <%= vagrantPath %> && vagrant rsync"
      }
    }
  });

  // Load plugins.
  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Register tasks.
  grunt.registerTask('default', ['watch']);
};
