# Déploiement avec Ansible

## Prérequis

- [ansible](https://docs.ansible.com/ansible/latest/index.html)

## Installer Ansible

> Exemples sur Ubuntu

### Avec pipx

Sur Ubuntu 24.04 et suivants, c'est pratique d'installer Ansible avec [pipx](https://pipx.pypa.io/) :

> [!TIP]
> [pipx](https://pipx.pypa.io/stable/installation/) est l'outil moderne du groupe Python packaging de la fondation Python pour installer proprement les outils en ligne de commande en respectant les pratiques et contraintes des différents OS.  
> Pour l'installer sur Ubuntu :  
>
> ```sh
> sudo apt install pipx
> pipx ensurepath
> ```

Puis, après avoir redémarré son terminal :

```sh
pipx install ansible-core ansible-lint pre-commit
```

### Avec un environnement virtuel

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

### Installer les rôles et collections Ansible

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
geotribu_prod | SUCCESS => {
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
> ansible -i inventory.yml geotribu_prod -a "sudo -l"
geotribu_prod | CHANGED | rc=0 >>
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
Enter passphrase for key '/home/jmo/.ssh/id_rsa_elgeopaso': ok: [geotribu_prod]

ok: [elgeopaso1804]

TASK [Ping l'hôte] *************************************************************************************************************************
ok: [geotribu_prod]
ok: [elgeopaso1804]

TASK [Affiche message de base] *************************************************************************************************************
ok: [elgeopaso1804] => {
    "msg": "Salut le serveur de GeoRezo"
}
ok: [geotribu_prod] => {
    "msg": "Salut le serveur de GeoRezo"
}

PLAY RECAP *********************************************************************************************************************************
elgeopaso1804              : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
geotribu_prod              : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```

### Lancer le playbook pour la production

```sh
ansible-playbook -i inventory.yml playbook.yml --ask-vault-pass -l geotribu_prod
```

Ou si le mot de passe du vault est dans le fichier `.ansible-vault.pass` :

```sh
ansible-playbook -i inventory.yml playbook.yml --vault-password-file .ansible-vault.pass -l geotribu_prod
```

Avec seulement certaines rôles :

```sh
ansible-playbook -i inventory.yml playbook.yml --vault-password-file .ansible-vault.pass -t cdn -l geotribu_prod -vv
```

### Gestion des secrets

Les mots de passe et autres données sensibles sont chiffrées à l'aide de l'utilitaire [`ansible-vault`](https://docs.ansible.com/ansible/latest/user_guide/vault.html) via un mot de passe maître (voir avec l'admin de Geotribu).

Il est possible de stocker le mot de passe maître à différents endroits :

- dans un fichier `.ansible-vault.pass` qui ne sera **jamais** envoyé ou ajouté à Git

#### Créer un nouveau secret

Pour ajouter un nouveau secret (mot de passe, token, etc.) qu'on appelle ici `mon_token_secret` :

1. Exécuter : `ansible-vault encrypt_string --vault-id default@.ansible-vault.pass --stdin-name 'mon_token_secret'`
1. Entrer la valeur du secret dans le prompt qui s'ouvre (fermer avec `Ctrl` + `d`)
1. Copier/coller le résultat dans le fichier de variables souhaité. Par exemple : `host_vars/geotribu_prod.yml`

#### Accèder à un secret

Pour accéder à un mot de passe dans le vault :

```sh
ansible localhost -m ansible.builtin.debug -a var="mon_token_secret" -e "@host_vars/geotribu_prod.yml" --vault-password-file .ansible-vault.pass
```

----

## Développement local

Il est recommandé d'utiliser une VM pour tester le déploiement sans risque.

### Prérequis

- [vagrant](https://developer.hashicorp.com/vagrant/install) et les paquets liés :
  - [libvirt](https://libvirt.org/) pour gérer les machines virtuelles :

    ```sh
    sudo apt install libvirt-daemon-system libvirt-dev
    sudo adduser $USER libvirt
    ```

  - le plugin libvirt de Vagrant :  

    ```sh
    vagrant plugin install vagrant-libvirt
    ```

- [virtualbox](https://doc.ubuntu-fr.org/%20virtualbox) comme provider
- si Ansible a été [installé avec pipx](#avec-pipx), ajouter passlib à son environnement :

    ```sh
    pipx inject ansible-core passlib
    ```

Penser à  se reloguer pour que les changements de groupe prennent effet.

> [!TIP]
> Il peut y avoir des conflits entre les modules du noyau de VirtualBox et ceux de KVM. Pour éviter ces conflits, il est recommandé de décharger le module `kvm_intel` avant de lancer Vagrant (valable tout le temps de la session utilisateur). Exemple pour les processeurs Intel :
>
> ```sh
> sudo modprobe -r kvm_intel
> ```

### Lancer la VM de test

```sh
cd ansible/
vagrant up --provision
```

```sh
ANSIBLE_ARGS="--vault-password-file .ansible-vault.pass -t base" vagrant provision vm_geotributest
```

Il peut-être nécessaire de redémarrer la machine virtuelle pour prendre en compte les changements (ajout de l'utilisateur à des groupes, etc.) :

```sh
vagrant halt
vagrant up
```
