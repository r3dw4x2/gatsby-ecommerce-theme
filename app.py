from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from models import DataEntry
from forms import DataEntryForm

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Initialize data entry model
data_entry_model = DataEntry()

@app.route('/')
def index():
    """Home page showing all data entries"""
    result = data_entry_model.get_all()
    entries = result.get('data', []) if result.get('success') else []
    
    if not result.get('success'):
        flash(f"Error loading entries: {result.get('error')}", 'error')
    
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    """Add new data entry"""
    form = DataEntryForm()
    
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'category': form.category.data,
            'description': form.description.data
        }
        
        result = data_entry_model.create(data)
        
        if result.get('success'):
            flash('Entry added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Error adding entry: {result.get("error")}', 'error')
    
    return render_template('add_entry.html', form=form)

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    """Edit existing data entry"""
    result = data_entry_model.get_by_id(entry_id)
    
    if not result.get('success') or not result.get('data'):
        flash('Entry not found', 'error')
        return redirect(url_for('index'))
    
    entry = result['data']
    form = DataEntryForm(obj=type('obj', (object,), entry)())
    
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'category': form.category.data,
            'description': form.description.data
        }
        
        update_result = data_entry_model.update(entry_id, data)
        
        if update_result.get('success'):
            flash('Entry updated successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Error updating entry: {update_result.get("error")}', 'error')
    
    return render_template('edit_entry.html', form=form, entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    """Delete data entry"""
    result = data_entry_model.delete(entry_id)
    
    if result.get('success'):
        flash('Entry deleted successfully!', 'success')
    else:
        flash(f'Error deleting entry: {result.get("error")}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/entries', methods=['GET'])
def api_get_entries():
    """API endpoint to get all entries"""
    result = data_entry_model.get_all()
    return jsonify(result)

@app.route('/api/entries', methods=['POST'])
def api_add_entry():
    """API endpoint to add new entry"""
    data = request.get_json()
    result = data_entry_model.create(data)
    return jsonify(result)

@app.route('/api/entries/<int:entry_id>', methods=['GET'])
def api_get_entry(entry_id):
    """API endpoint to get single entry"""
    result = data_entry_model.get_by_id(entry_id)
    return jsonify(result)

@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def api_update_entry(entry_id):
    """API endpoint to update entry"""
    data = request.get_json()
    result = data_entry_model.update(entry_id, data)
    return jsonify(result)

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def api_delete_entry(entry_id):
    """API endpoint to delete entry"""
    result = data_entry_model.delete(entry_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)