import sublime, sublime_plugin
import os
import subprocess
import threading
import re

class RailsMagicClipboardCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if self.view.file_name() and (self.view.file_name().endswith(".css.sass") or self.view.file_name().endswith(".js.coffee") or self.view.file_name().endswith(".html.haml")):
      self.convert_to_sass(sublime.get_clipboard())
    else:
      for region in self.view.sel():
        self.view.replace(edit, region, sublime.get_clipboard())

  def convert_to_sass(self, text):
    if (";" in text or "</" in text):
      thread = ExecSassCommand(
            self.get_cmd(),
            self.get_env(),
            text
        )
      thread.start()
      self.check_thread(thread)
    else:
      self.view.run_command('replace_text', {'text': sublime.get_clipboard()})

  def get_cmd(self):
    if(self.view.file_name().endswith(".css.sass")):
      return "sass-convert"
    elif (self.view.file_name().endswith(".js.coffee")):
      return "js2coffee"
    elif (self.view.file_name().endswith(".html.haml")):
      return "html2haml"
    else:
      sublime.error_message("Not sure how you got here, but you're trying to insert into an unsupported file type.")

  def get_env(self):
    env = os.environ.copy()
    self.settings = sublime.load_settings('Css2Sass.sublime-settings')
    if self.settings.get('path', False):
      env['PATH'] = self.settings.get('path')
    return env

  def check_thread(self, thread, i=0, dir=1):
    before = i % 8
    after = (7) - before
    if not after:
        dir = -1
    if not before:
        dir = 1
    i += dir

    self.view.set_status(
        'rails_magic_clipboard',
        'RailsMagicClipboard [%s=%s]' % (' ' * before, ' ' * after)
    )

    if thread.is_alive():
      return sublime.set_timeout(lambda: self.check_thread(thread, i, dir), 100)

    self.view.erase_status('rails_magic_clipboard')
    sass_text = self.handle_process(thread.returncode, thread.stdout, thread.stderr)
    self.view.run_command('replace_text', {'text': sass_text})

    return sass_text

  def handle_process(self, returncode, output, error):
      if type(output) is bytes:
        output = output.decode('utf-8')

      if type(error) is bytes:
        error = error.decode('utf-8')

      if returncode != 0:
        print("Error code: {}".format(returncode))
        self.view.run_command('replace_text', {'text': sublime.get_clipboard()})
        sublime.error_message(error)
        return False

      output = '\n'.join(output.splitlines())
      return output

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
