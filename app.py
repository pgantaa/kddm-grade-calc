# Assignment and Exam Score Calculator
# Goal: Help users determine the minimum exam score needed to achieve an "A" (>90%)

from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<title>Grade Calculator</title>
<h2>Assignment & Exam Target Calculator</h2>
<form action="/" method="post">
  <label>Enter either:</label><br>
  <b>1. Total assignment score out of 40:</b><br>
  <input type="number" step="0.1" name="total_score" placeholder="e.g., 37"><br><br>
  <b>OR</b><br>
  <b>2. Enter 5 assignment scores separately (out of 10):</b><br>
  <input type="number" step="0.1" name="a1" placeholder="Assignment 1">
  <input type="number" step="0.1" name="a2" placeholder="Assignment 2">
  <input type="number" step="0.1" name="a3" placeholder="Assignment 3">
  <input type="number" step="0.1" name="a4" placeholder="Assignment 4">
  <input type="number" step="0.1" name="a5" placeholder="Assignment 5"><br><br>
  <input type="submit" value="Calculate">
</form>

{% if result %}
<hr>
<h3>{{ result }}</h3>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def calculate():
    result = None
    if request.method == 'POST':
        try:
            total_score = request.form.get('total_score')
            a1 = request.form.get('a1')
            a2 = request.form.get('a2')
            a3 = request.form.get('a3')
            a4 = request.form.get('a4')
            a5 = request.form.get('a5')

            if total_score:
                assignment_total = float(total_score)
            else:
                scores = [float(x) for x in [a1, a2, a3, a4, a5] if x]
                assignment_total = sum(scores)

            assignment_percentage = (assignment_total / 40) * 100
            weighted_assignment = assignment_percentage * 0.4

            needed_total = 90
            needed_from_exam = needed_total - weighted_assignment
            min_exam_score = needed_from_exam / 0.6

            if min_exam_score > 100:
                result = f"Unfortunately, it is not mathematically possible to achieve an A. You would need more than 100 in the exam."
            else:
                result = f"You need at least {min_exam_score:.2f}% in the exam to achieve an A (>90% total)."

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template_string(HTML_PAGE, result=result)

if __name__ == '__main__':
    app.run(debug=True)
