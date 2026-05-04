Earthkit-climate documentation
==============================

.. important::

   This software is **Emerging** and subject to ECMWF's guidelines on `Software Maturity <https://github.com/ecmwf/codex/raw/refs/heads/main/Project%20Maturity>`_.


.. admonition:: Help us improve!
   :class: tip survey

   Share your experience and needs (3-5 minutes survey)

   .. raw:: html

      <a href="https://ec.europa.eu/eusurvey/runner/user_feedback_integration" class="survey-button">Start Survey</a>


**earthkit-climate** is the package responsible for climate index calculations within the earthkit ecosystem. It includes a wrapper prototype that allows the use of the `xclim <https://xclim.readthedocs.io/en/stable/>`_ Python package to compute a large amount of pre-defined climate indices used by the climate science community, and to define new ones.


.. grid:: 1
   :gutter: 2

   .. grid-item-card:: Why earthkit-climate?
      :img-top:  _static/earthkit-climate-grey.svg
      :link: why
      :link-type: doc
      :class-card: sd-shadow-sm

      The motivation and key features of earthkit-climate.


.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: Installation and Getting Started
      :img-top: _static/rocket.svg
      :link: getting-started
      :link-type: doc
      :class-card: sd-shadow-sm

      New to earthkit-climate? Start here with installation and a quick overview.

   .. grid-item-card:: Frequently Asked Questions
      :img-top: _static/message-question.svg
      :link: faq
      :link-type: doc
      :class-card: sd-shadow-sm

      The most common questions, answered.

   .. grid-item-card:: Tutorials
      :img-top: _static/book.svg
      :link: tutorials/index
      :link-type: doc
      :class-card: sd-shadow-sm

      Step-by-step guides to learn earthkit-climate.

   .. grid-item-card:: How-tos
      :img-top: _static/tool.svg
      :link: how-tos/index
      :link-type: doc
      :class-card: sd-shadow-sm

      Practical recipes for common tasks.

   .. grid-item-card:: Concepts
      :img-top: _static/bulb.svg
      :link: concepts/index
      :link-type: doc
      :class-card: sd-shadow-sm

      Understand the core ideas behind earthkit-climate.

   .. grid-item-card:: API Reference Guide
      :img-top: _static/brackets-contain.svg
      :link: api-reference
      :link-type: doc
      :class-card: sd-shadow-sm

      Detailed documentation of all functions and classes.


**Support**

Have a feature request or found a bug? Feel free to open an
`issue <https://github.com/ecmwf/earthkit-climate/issues/new/choose>`_.


.. toctree::
   :maxdepth: 2
   :hidden:

   why

.. toctree::
   :caption: User guide
   :maxdepth: 2
   :hidden:

   getting-started
   faq
   tutorials/index
   how-tos/index
   concepts/index
   api-reference


.. toctree::
   :caption: Developer guide
   :maxdepth: 2
   :hidden:

   development


.. toctree::
   :maxdepth: 2
   :caption: Extras
   :hidden:

   release-notes/index
   licence
   genindex
