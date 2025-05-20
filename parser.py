import re

class SANParser:
    def __init__(self):
        # Expresiones regulares para jugadas válidas según la BNF simplificada
        self.regex_turno = re.compile(r'(?P<num>\d+)\.\s*(?P<white>\S+)(?:\s+(?P<black>\S+))?')
        self.regex_enroque = re.compile(r'^(O-O|O-O-O)$')
        self.regex_pieza = r'[KQRBN]'
        self.regex_casilla = r'[a-h][1-8]'
        self.regex_captura = r'x'
        self.regex_promocion = r'=([QRBN])'
        self.regex_jaque = r'[+#]?'
        self.regex_peon = r'[a-h]'
        # Movimiento de pieza: Pieza + (desambiguación)? + (captura)? + casilla + (promoción)? + (jaque)?
        self.regex_mov_pieza = re.compile(rf'^{self.regex_pieza}([a-h1-8]?)({self.regex_captura})?{self.regex_casilla}({self.regex_promocion})?{self.regex_jaque}$')
        # Movimiento de peón: avance o captura
        self.regex_peon_avance = re.compile(rf'^{self.regex_casilla}({self.regex_promocion})?{self.regex_jaque}$')
        self.regex_peon_captura = re.compile(rf'^{self.regex_peon}{self.regex_captura}{self.regex_casilla}({self.regex_promocion})?{self.regex_jaque}$')

    def parse(self, san_text):
        """
        Recibe el texto de la partida en SAN y valida cada turno y jugada.
        Devuelve una lista de tuplas (num_turno, jugada_blanca, jugada_negra) o un error.
        """
        # Unir todas las líneas en un solo string y eliminar espacios extra
        san_text = ' '.join(san_text.strip().split())
        moves = []
        # Buscar todos los turnos en el texto
        for match in self.regex_turno.finditer(san_text):
            num_turno = match.group('num')
            jugada_blanca = match.group('white')
            jugada_negra = match.group('black') if match.group('black') else None
            print(f"Turno {num_turno}: blanca='{jugada_blanca}', negra='{jugada_negra}'")  # DEPURACIÓN
            # Validar jugadas
            if not self.is_valid_jugada(jugada_blanca):
                return f"Jugada blanca inválida en el turno {num_turno}: '{jugada_blanca}'"
            if jugada_negra and not self.is_valid_jugada(jugada_negra):
                return f"Jugada negra inválida en el turno {num_turno}: '{jugada_negra}'"
            moves.append((num_turno, jugada_blanca, jugada_negra))
        return moves

    def is_valid_jugada(self, jugada):
        # Enroque
        if self.regex_enroque.match(jugada):
            return True
        # Movimiento de pieza
        if self.regex_mov_pieza.match(jugada):
            return True
        # Movimiento de peón avance
        if self.regex_peon_avance.match(jugada):
            return True
        # Movimiento de peón captura
        if self.regex_peon_captura.match(jugada):
            return True
        return False 