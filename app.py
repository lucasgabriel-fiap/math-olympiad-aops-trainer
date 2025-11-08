from flask import Flask, jsonify, render_template
from flask_cors import CORS
from datasets import load_dataset
import random

app = Flask(__name__)
CORS(app)

print("⚙️ Carregando MATH Competition Dataset...")
dataset = load_dataset("qwedsacf/competition_math")
train_data = dataset['train']
print(f"✅ {len(train_data)} problemas REAIS carregados!")

CATEGORIES = ['Algebra', 'Counting & Probability', 'Geometry', 
              'Intermediate Algebra', 'Number Theory', 'Prealgebra', 'Precalculus']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/question/<category>')
def get_question(category='all'):
    """Retorna um problema REAL do dataset"""
    try:
        if category == 'all':
            problems = train_data
        else:
            problems = [p for p in train_data if p['type'] == category]
        
        if not problems:
            return jsonify({'success': False, 'error': 'Categoria não encontrada'}), 404
        
        problem = random.choice(problems)
        
        return jsonify({
            'success': True,
            'problem': problem['problem'],
            'solution': problem['solution'],
            'level': problem['level'],
            'type': problem['type']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Estatísticas do dataset"""
    stats = {}
    for cat in CATEGORIES:
        count = len([p for p in train_data if p['type'] == cat])
        stats[cat] = count
    
    return jsonify({
        'total': len(train_data),
        'categories': stats
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 MATH Competition Viewer - Zero-Error Mode")
    print("="*60)
    print(f"📚 Problemas carregados: {len(train_data)}")
    print("🎨 Diagramas: Placeholder Mode (100% confiável)")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)