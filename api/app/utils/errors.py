def error_404_not_found(description):
    return {
        'error': description or 'Não encontrado'
    }

def error_403_forbidden(description):
    return {
        'error': description or 'Você não tem permissões para entrar nessa rota, faça o login e tente novamente.'
    }