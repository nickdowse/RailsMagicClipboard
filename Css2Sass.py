import sublime, sublime_plugin
import os
import subprocess
import threading
import re

class CssToSassCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if self.view.file_name().endswith(".css.sass"):
      edit_sass = edit
      self.convert_to_sass(sublime.get_clipboard(), edit_sass)
    else:
      for region in self.view.sel():
        self.view.replace(edit, region, sublime.get_clipboard())

  def convert_to_sass(self, text, edit_sass):
    if ";" in text:
      thread = ExecSassCommand(
            'sass-convert',
            self.get_env(),
            text
        )
      thread.start()
      sass_text = self.check_thread(thread, edit_sass)



  def check_thread(self, thread, edit_sass, i=0, dir=1):
    before = i % 8
    after = (7) - before
    if not after:
        dir = -1
    if not before:
        dir = 1
    i += dir

    self.view.set_status(
        'css2sass',
        'Css2Sass [%s=%s]' % (' ' * before, ' ' * after)
    )

    if thread.is_alive():
      return sublime.set_timeout(lambda: self.check_thread(thread, edit_sass, i, dir), 100)

    self.view.erase_status('css2sass')
    sass_text = self.handle_process(thread.returncode, thread.stdout, thread.stderr)
    self.view.run_command('replace_text', {'text': sass_text})

    return sass_text

  def handle_process(self, returncode, output, error):
      if type(output) is bytes:
        output = output.decode('utf-8')

      if type(error) is bytes:
        error = error.decode('utf-8')

      if returncode != 0:
        return False

      output = '\n'.join(output.splitlines())
      return output

  def get_env(self):
    env = os.environ.copy()
    if self.settings.get('path', False):
      env['PATH'] = self.settings.get('path')
    return env

class ExecSassCommand(threading.Thread):

  def __init__(self, cmd, env, stdin):
    self.cmd = cmd
    self.env = env
    self.stdin = stdin
    self.returncode = 0
    self.stdout = None
    self.stderr = None

    threading.Thread.__init__(self)

  def run(self):

    try:
      process = subprocess.Popen(
          self.cmd,
          env=self.env,
          shell=sublime.platform() == 'windows',
          stdin=subprocess.PIPE,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE
      )
      (self.stdout, self.stderr) = process.communicate(input=self.stdin.encode('utf-8'))
      self.stdout = self.stdout.decode("utf-8")
      self.returncode = process.returncode
    except OSError as e:
      self.stderr = str(e)
      self.returncode = 1

class ReplaceTextCommand(sublime_plugin.TextCommand):
  def run(self, edit, text=None):
    for region in self.view.sel():
      self.view.replace(edit, region, text)
