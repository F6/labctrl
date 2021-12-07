from bokeh.models.widgets import Div
from tornado import gen
from functools import partial

from main_doc import doc

task_template = """
<div class="accordion" id="accordionTaskOverview">
  <div class="accordion-item">
    <div class="accordion-header" id="headingOne">
      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
        {running} tasks running
      </button>
    </div>
    <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionTaskOverview">
      <div class="accordion-body">
        No preview available
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <div class="accordion-header" id="headingTwo">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
        {queued} tasks queued
      </button>
    </div>
    <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionTaskOverview">
      <div class="accordion-body">
        No preview available
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <div class="accordion-header" id="headingThree">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
        {finished} tasks finished
      </button>
    </div>
    <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionTaskOverview">
      <div class="accordion-body">
        No preview available
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <div class="accordion-header" id="headingFour">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
        {failed} tasks failed
      </button>
    </div>
    <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour" data-bs-parent="#accordionTaskOverview">
      <div class="accordion-body">
        No preview available
      </div>
    </div>
  </div>
</div>
"""


class TasksOverview:
    def __init__(self) -> None:
        self.template = task_template
        self.html = self.template.format(
            running=0,
            queued=0,
            finished=0,
            failed=0
            )
        self.div = Div(text=self.html, sizing_mode="stretch_width")

    def update(self, running, queued, finished, failed):
        self.html = self.template.format(
            running=running,
            queued=queued,
            finished=finished,
            failed=failed
            )
        doc.add_next_tick_callback(self.update_callback)

    @gen.coroutine
    def update_callback(self):
        self.div.text = self.html

taskoverview = TasksOverview()

