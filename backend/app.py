from flask import Flask, jsonify, request, send_from_directory
import os
import json

# Set up Flask app with proper static folder configuration
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_static = os.path.join(project_root, 'frontend', 'static')
app = Flask(__name__, static_folder=frontend_static, static_url_path='/static')

@app.route('/')
def index():
    return send_from_directory('../frontend', 'dashboard.html')

@app.route('/sbox-analysis')
def sbox_analysis():
    return send_from_directory('../frontend', 'sbox-analysis.html')

@app.route('/text-encryption')
def text_encryption():
    return send_from_directory('../frontend', 'text-encryption.html')

@app.route('/image-encryption')
def image_encryption():
    return send_from_directory('../frontend', 'image-encryption.html')

@app.route('/api/sboxes', methods=['GET'])
def get_sboxes():
    """Returns list of available predefined S-boxes"""
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'sboxes')
    sbox_files = [f for f in os.listdir(sboxes_dir) if f.endswith('.json')]

    sboxes_info = []
    for filename in sbox_files:
        filepath = os.path.join(sboxes_dir, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Create an ID from the filename without extension
            sbox_id = os.path.splitext(filename)[0]
            sboxes_info.append({
                'id': sbox_id,
                'name': data.get('name', ''),
                'source': data.get('source', ''),
                'description': data.get('description', '')
            })

    return jsonify(sboxes_info)

@app.route('/api/sbox/<sbox_id>', methods=['GET'])
def get_sbox_by_id(sbox_id):
    """Returns the content of a specific S-box by ID"""
    filepath = os.path.join(os.path.dirname(__file__), 'sboxes', f'{sbox_id}.json')

    if not os.path.exists(filepath):
        return jsonify({"error": f"S-box '{sbox_id}' not found"}), 404

    with open(filepath, 'r') as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/api/compute', methods=['POST'])
def compute_metrics():
    """Computes all S-box cryptographic metrics"""
    try:
        data = request.get_json()

        if not data or 'sbox' not in data:
            return jsonify({"ok": False, "error": "Missing 'sbox' in request body"}), 400

        sbox = data['sbox']

        # Validate input
        if not isinstance(sbox, list) or len(sbox) != 256:
            return jsonify({"ok": False, "error": "S-box must be a list of 256 integers"}), 400

        for val in sbox:
            if not isinstance(val, int) or val < 0 or val > 255:
                return jsonify({"ok": False, "error": "All values must be integers between 0 and 255"}), 400

        # Import metric functions
        from sbox_metrics.nl import compute_nl
        from sbox_metrics.sac import compute_sac
        from sbox_metrics.bic import compute_bic_nl, compute_bic_sac
        from sbox_metrics.lap import compute_lap
        from sbox_metrics.dap import compute_dap
        from sbox_metrics.du import compute_du
        from sbox_metrics.ad import compute_ad
        from sbox_metrics.to_metric import compute_to
        from sbox_metrics.ci import compute_ci

        # Calculate metrics
        metrics = {
            "NL": compute_nl(sbox),
            "SAC": compute_sac(sbox),
            "BIC_NL": compute_bic_nl(sbox),
            "BIC_SAC": compute_bic_sac(sbox),
            "LAP": compute_lap(sbox),
            "DAP": compute_dap(sbox),
            "DU": compute_du(sbox),
            "AD": compute_ad(sbox),
            "TO": compute_to(sbox),
            "CI": compute_ci(sbox)
        }

        return jsonify({"ok": True, "metrics": metrics})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# Import affine generator
from affine_generator import generate_affine_sbox, get_predefined_matrices

@app.route('/api/generate-affine-sbox', methods=['POST'])
def generate_affine():
    """Generate S-box using affine transformation"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"ok": False, "error": "Missing request body"}), 400
        
        # Get matrix value (can be hex string or integer)
        matrix = data.get('matrix', '0x57')
        if isinstance(matrix, str):
            matrix_value = int(matrix, 16) if matrix.startswith('0x') else int(matrix)
        else:
            matrix_value = int(matrix)
        
        # Get additive constant (default: 0x63 for standard AES)
        constant = int(data.get('constant', 0x63))
        
        # Validate inputs
        if not (0 <= matrix_value <= 255):
            return jsonify({"ok": False, "error": "Matrix value must be between 0 and 255"}), 400
        
        if not (0 <= constant <= 255):
            return jsonify({"ok": False, "error": "Additive constant must be between 0 and 255"}), 400
        
        # Generate S-box
        sbox = generate_affine_sbox(matrix_value, constant)
        
        return jsonify({
            "ok": True,
            "sbox": sbox,
            "matrix": hex(matrix_value),
            "constant": constant
        })
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/affine-matrices', methods=['GET'])
def get_affine_matrices():
    """Get list of predefined affine matrices"""
    try:
        matrices = get_predefined_matrices()
        return jsonify({"ok": True, "matrices": matrices})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# Import crypto engine
from crypto_engine import SPNCipher, get_available_sboxes, get_sbox_by_id, validate_sbox

# Import image crypto engine
from image_crypto_engine import ImageSPNCipher, get_sbox_by_id as get_sbox_by_id_img, validate_sbox as validate_sbox_img

@app.route('/api/encrypt', methods=['POST'])
def encrypt_text():
    """Enkripsi teks menggunakan S-box tertentu"""
    try:
        data = request.get_json()

        if not data or 'plaintext' not in data or 'key' not in data or 'sbox_id' not in data:
            return jsonify({"ok": False, "error": "Missing 'plaintext', 'key', or 'sbox_id' in request body"}), 400

        plaintext = data['plaintext']
        key = data['key']
        sbox_id = data['sbox_id']

        # Ambil S-box berdasarkan ID
        sbox = get_sbox_by_id(sbox_id)

        # Validasi S-box
        if not validate_sbox(sbox):
            return jsonify({"ok": False, "error": "Invalid S-box format"}), 400

        # Buat cipher dan enkripsi
        cipher = SPNCipher(sbox)
        ciphertext = cipher.encrypt(plaintext, key)

        return jsonify({"ok": True, "ciphertext": ciphertext})

    except FileNotFoundError:
        return jsonify({"ok": False, "error": f"S-box '{sbox_id}' not found"}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/decrypt', methods=['POST'])
def decrypt_text():
    """Dekripsi teks menggunakan S-box tertentu"""
    try:
        data = request.get_json()

        if not data or 'ciphertext' not in data or 'key' not in data or 'sbox_id' not in data:
            return jsonify({"ok": False, "error": "Missing 'ciphertext', 'key', or 'sbox_id' in request body"}), 400

        ciphertext = data['ciphertext']
        key = data['key']
        sbox_id = data['sbox_id']

        # Ambil S-box berdasarkan ID
        sbox = get_sbox_by_id(sbox_id)

        # Validasi S-box
        if not validate_sbox(sbox):
            return jsonify({"ok": False, "error": "Invalid S-box format"}), 400

        # Buat cipher dan dekripsi
        cipher = SPNCipher(sbox)
        plaintext = cipher.decrypt(ciphertext, key)

        return jsonify({"ok": True, "plaintext": plaintext})

    except FileNotFoundError:
        return jsonify({"ok": False, "error": f"S-box '{sbox_id}' not found"}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/custom_encrypt', methods=['POST'])
def encrypt_with_custom_sbox():
    """Enkripsi teks menggunakan S-box kustom"""
    try:
        data = request.get_json()

        if not data or 'plaintext' not in data or 'key' not in data or 'sbox' not in data:
            return jsonify({"ok": False, "error": "Missing 'plaintext', 'key', or 'sbox' in request body"}), 400

        plaintext = data['plaintext']
        key = data['key']
        sbox = data['sbox']

        # Validasi S-box kustom
        if not validate_sbox(sbox):
            return jsonify({"ok": False, "error": "Invalid S-box format. Must contain 256 unique integers between 0-255."}), 400

        # Buat cipher dan enkripsi
        cipher = SPNCipher(sbox)
        ciphertext = cipher.encrypt(plaintext, key)

        return jsonify({"ok": True, "ciphertext": ciphertext})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/custom_decrypt', methods=['POST'])
def decrypt_with_custom_sbox():
    """Dekripsi teks menggunakan S-box kustom"""
    try:
        data = request.get_json()

        if not data or 'ciphertext' not in data or 'key' not in data or 'sbox' not in data:
            return jsonify({"ok": False, "error": "Missing 'ciphertext', 'key', or 'sbox' in request body"}), 400

        ciphertext = data['ciphertext']
        key = data['key']
        sbox = data['sbox']

        # Validasi S-box kustom
        if not validate_sbox(sbox):
            return jsonify({"ok": False, "error": "Invalid S-box format. Must contain 256 unique integers between 0-255."}), 400

        # Buat cipher dan dekripsi
        cipher = SPNCipher(sbox)
        plaintext = cipher.decrypt(ciphertext, key)

        return jsonify({"ok": True, "plaintext": plaintext})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# Endpoint untuk enkripsi/dekripsi gambar
@app.route('/api/image/encrypt', methods=['POST'])
def encrypt_image():
    """Enkripsi gambar menggunakan S-box tertentu"""
    try:
        if 'image' not in request.files:
            return jsonify({"ok": False, "error": "Missing 'image' file in request"}), 400

        if 'key' not in request.form or 'sbox_id' not in request.form:
            return jsonify({"ok": False, "error": "Missing 'key' or 'sbox_id' in request form"}), 400

        image_file = request.files['image']
        key = request.form['key']
        sbox_id = request.form['sbox_id']

        if image_file.filename == '':
            return jsonify({"ok": False, "error": "No image file selected"}), 400

        # Ambil S-box berdasarkan ID
        sbox = get_sbox_by_id_img(sbox_id)

        # Validasi S-box
        if not validate_sbox_img(sbox):
            return jsonify({"ok": False, "error": "Invalid S-box format"}), 400

        # Buat cipher dan enkripsi gambar
        cipher = ImageSPNCipher(sbox)

        # Baca file gambar ke buffer
        image_bytes = image_file.read()

        # Enkripsi gambar
        encrypted_image_bytes = cipher.encrypt_image_bytes_v2(image_bytes, key)

        # Kembalikan gambar terenkripsi
        from flask import Response
        return Response(
            encrypted_image_bytes,
            mimetype='image/png',
            headers={'Content-Disposition': 'attachment; filename=encrypted_image.png'}
        )

    except FileNotFoundError:
        return jsonify({"ok": False, "error": f"S-box '{sbox_id}' not found"}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/image/decrypt', methods=['POST'])
def decrypt_image():
    """Dekripsi gambar menggunakan S-box tertentu"""
    try:
        if 'image' not in request.files:
            return jsonify({"ok": False, "error": "Missing 'image' file in request"}), 400

        if 'key' not in request.form or 'sbox_id' not in request.form:
            return jsonify({"ok": False, "error": "Missing 'key' or 'sbox_id' in request form"}), 400

        image_file = request.files['image']
        key = request.form['key']
        sbox_id = request.form['sbox_id']

        if image_file.filename == '':
            return jsonify({"ok": False, "error": "No image file selected"}), 400

        # Ambil S-box berdasarkan ID
        sbox = get_sbox_by_id_img(sbox_id)

        # Validasi S-box
        if not validate_sbox_img(sbox):
            return jsonify({"ok": False, "error": "Invalid S-box format"}), 400

        # Buat cipher dan dekripsi gambar
        cipher = ImageSPNCipher(sbox)

        # Baca file gambar ke buffer
        image_bytes = image_file.read()

        # Dekripsi gambar
        decrypted_image_bytes = cipher.decrypt_image_bytes_v2(image_bytes, key)

        # Kembalikan gambar terdekripsi
        from flask import Response
        return Response(
            decrypted_image_bytes,
            mimetype='image/png',
            headers={'Content-Disposition': 'attachment; filename=decrypted_image.png'}
        )

    except FileNotFoundError:
        return jsonify({"ok": False, "error": f"S-box '{sbox_id}' not found"}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)