# Déploiement avec Ansible

## Prérequis

- [ansible]()

    Sur Ubuntu 24.04, c'est pratique d'installer Ansible avec [pipx](https://pipx.pypa.io/) :

    > [!TIP]
    > [pipx](https://pipx.pypa.io/stable/installation/) est l'outil moderne du groupe Python packaging de la fondation Python pour installer proprement les outils en ligne de commande en respectant les pratiques et contraintes des différents OS.  
    > Pour l'installer sur Ubuntu :  
    >
    > ```sh
    > sudo apt install pipx
    > pipx ensurepath
    > ```

    Puis :

    ```sh
    pipx install ansible-core ansible-lint pre-commit
    ```

- [vagrant](https://developer.hashicorp.com/vagrant/install) et [virtualbox](https://doc.ubuntu-fr.org/%20virtualbox) pour le développement local

## Installer Ansible - Exemple sur Ubuntu

Créer un environnement virtuel :

```sh
python3 -m venv .venv
source .venv/bin/activate
```

MAJ l'outillage puis installer Ansible :

```sh
python -m pip install -U pip
python -m pip install -U setuptools wheel
python -m pip install -U -r ansible/requirements.txt
```

Installer les rôles et collections Ansible :

```sh
ansible-galaxy install -r ansible/requirements.yml
```

Se déplacer dans ce dossier :

```sh
cd ansible/
```

Sauf mention contraire, les commandes suivantes sont à mener dans cet environnement virtuel et dans ce dossier.

## Vérifier sa configuration SSH

Voir le README principal.

## Adapter le fichier `inventory.yml` si besoin

Adaptations possibles :

- la valeur des clés `ansible_host` doit correspondre aux hosts déclarés dans le `~/.ssh.config`

## Tester si Ansible se connecte et s'exécute correctement

Exécuter un ping :

```sh
> ansible -i inventory.yml all -m ping
elgeopaso2204 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}

elgeopaso1804 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

Vérifier l'exécution en mode `sudo` :

```sh
> ansible -i inventory.yml elgeopaso2204 -a "sudo -l"
elgeopaso2204 | CHANGED | rc=0 >>
Matching Defaults entries for geotribu on geotribu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User geotribu may run the following commands on geotribu:
    (ALL) NOPASSWD: ALL
```

Lancer le playbook de test :

```sh
> ansible-playbook -i inventory.yml playbook-test.yml

PLAY [Playbook de test] ***********************************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************************
Enter passphrase for key '/home/jmo/.ssh/id_rsa_elgeopaso': ok: [elgeopaso2204]

ok: [elgeopaso1804]

TASK [Ping l'hôte] *************************************************************************************************************************
ok: [elgeopaso2204]
ok: [elgeopaso1804]

TASK [Affiche message de base] *************************************************************************************************************
ok: [elgeopaso1804] => {
    "msg": "Salut le serveur de GeoRezo"
}
ok: [elgeopaso2204] => {
    "msg": "Salut le serveur de GeoRezo"
}

PLAY RECAP *********************************************************************************************************************************
elgeopaso1804              : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
elgeopaso2204              : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```

### Lancer le playbook

```sh
ansible-playbook -i inventory.yml playbook.yml --ask-vault-pass
```

Ou si le mot de passe du vault est dans le fichier `password_file` :

```sh
ansible-playbook -i inventory.yml playbook.yml --vault-password-file password_file
```

### Gestion des secrets

Les mots de passe et autres données sensibles sont chiffrées à l'aide de l'utilitaire [`ansible-vault`](https://docs.ansible.com/ansible/latest/user_guide/vault.html) via un mot de passe maître (voir avec l'admin de Geotribu).

Il est possible de stocker le mot de passe maître à différents endroits :

- dans un fichier `password_file` qui ne sera **jamais** envoyé ou ajouté à Git

#### Créer un nouveau secret

Pour ajouter un nouveau secret (mot de passe, token, etc.) qu'on appelle ici `mon_token_secret` :

1. Exécuter : `ansible-vault encrypt_string --vault-id default@password_file --stdin-name 'mon_token_secret'`
1. Entrer la valeur du secret dans le prompt qui s'ouvre (fermer avec `Ctrl` + `d`)
1. Copier/coller le résultat dans le fichier de variables souhaité. Par exemple : `host_vars/elgeopaso2204.yml`

#### Accèder à un secret

Pour accéder à un mot de passe dans le vault :

```sh
ansible localhost -m ansible.builtin.debug -a var="mon_token_secret" -e "@host_vars/elgeopaso2204.yml" --vault-password-file password_file
```

----

## Développement local

Il est possible d'utiliser une VM pour tester le déploiement sans risque :

```sh
vagrant up --provision
```
