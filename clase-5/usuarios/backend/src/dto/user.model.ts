export interface CreateUserDTO {
  nombre: string;
  apellido: string;
  email: string;
  password: string;
  role?: string;
}

export interface UpdateUserDTO {
  nombre?: string;
  apellido?: string;
  email?: string;
  password?: string;
  role?: string;
  active?: boolean;
}

export interface LoginDTO {
  email: string;
  password: string;
}

export interface UserResponseDTO {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  role: string;
  active: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface LoginResponseDTO {
  token: string;
  user: UserResponseDTO;
}
